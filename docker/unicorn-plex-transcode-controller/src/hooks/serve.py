#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
import sys


class Controller(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def sync_transcoder_labels(self, request):
        logger = logging.getLogger("unicorn-transcoder-controller")
        pod = request["object"]
        pod_name = pod["metadata"]["name"]
        logger.info("Handling Transcoder Label For: %s", pod_name)
        label_key = pod["metadata"]["annotations"]["transcoder-name-label"]

        logger.info("Setting Label %s: %s", label_key, pod_name)
        labels = {
            label_key: pod_name
        }

        return {"labels": labels}

    def sync_transcoder_ingress(self, request):
        logger = logging.getLogger("unicorn-transcoder-controller")
        statefulset = request["object"]
        statefulset_annotations = statefulset["metadata"]["annotations"]
        logger.info("Creating Ingress for Statefulset...")
        label_key = statefulset_annotations["transcoder-pod-name-label"]
        ports = statefulset_annotations["transcoder-pod-port"]
        transcode_domain = statefulset_annotations["transcode-domain"]

        attachments = []
        for i in range(0, statefulset["spec"]["replicas"]):
            service_port = ports.split(":")
            transcode_hostname = statefulset["metadata"]["name"] + "-" \
                + str(i) + '.' + transcode_domain
            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": statefulset["metadata"]["name"] + "-" + str(i),
                    "labels": {"transcoder-ingress": "transcoder-service"}
                },
                "spec": {
                    "selector": {
                        label_key: statefulset["metadata"]["name"] +
                        "-" + str(i)
                    },
                    "ports": [
                        {
                            "port": int(service_port[0]),
                            "targetPort": int(service_port[1])
                        }
                    ]
                }
            }
            ingress = {
                "apiVersion": "extensions/v1beta1",
                "kind": "Ingress",
                "metadata": {
                    "name": statefulset["metadata"]["name"] + "-" + str(i),
                    "labels": {"transcoder-ingress": "transcoder-ingress"},
                    "annotations": {
                        "kubernetes.io/ingress.class": "nginx",
                        "kubernetes.io/tls-acme": "true",
                        "cert-manager.io/cluster-issuer": "letsencrypt-prod",
                        "nginx.ingress.kubernetes.io/proxy-http-version":
                            "1.1"
                    }
                },
                "spec": {
                    "tls": [
                        {
                            "hosts": [
                                transcode_hostname
                            ],
                            "secretName": statefulset["metadata"]["name"] + "-"
                            + str(i) + "-tls",
                        }
                    ],
                    "rules": [
                        {
                            "host": transcode_hostname,
                            "http":
                            {
                                "paths": [
                                    {"path": "/",
                                     "backend": {
                                        "serviceName":
                                        statefulset["metadata"]["name"] + "-"
                                        + str(i),
                                        "servicePort": int(service_port[0])
                                     }}
                                ]
                            }
                        }
                    ]
                }
            }

            attachments.append(ingress)
            attachments.append(service)
        return {"attachments": attachments}

    def finalize_transcoder_ingress(self, request):
        attachments = []
        services_finalized = len(request["attachments"]["Service.v1"]) == 0
        ingress_finalized = \
            len(request["attachments"]["Ingress.extensions/v1beta1"]) \
            == 0
        finalized = (services_finalized and ingress_finalized)

        return {"attachments": attachments, "finalized": finalized}

    def do_POST(self):
        logger = logging.getLogger("unicorn-transcoder-controller")
        request = json.loads(
            self.rfile.read(
                int(self.headers.get_all("Content-Length")[0])
            )
        )
        logger.debug("Current Path: %s", self.path)
        logger.debug("Current Request: %s", json.dumps(request))
        if self.path == "/sync-transcoder-labels":
            response = self.sync_transcoder_labels(request)
        elif self.path == "/sync-transcoder-ingress":
            response = self.sync_transcoder_ingress(request)
        elif self.path == "/finalize-transcoder-ingress":
            response = self.finalize_transcoder_ingress(request)

        if response is not None:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(500)


def run_controller():
    formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(stream=sys.stdout,
                        format=formatter,
                        level=logging.DEBUG)
    logger = logging.getLogger("unicorn-transcoder-controller")

    logger.info("Starting controller...")
    server_conn = ('', 80)
    controller = HTTPServer(server_conn, Controller)
    try:
        controller.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down controller...")
        controller.server_close()
    logger.info("Shutdown")


if __name__ == "__main__":
    run_controller()
