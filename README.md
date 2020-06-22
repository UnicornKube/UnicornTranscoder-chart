Unicorn Transcoder on K8s
=========================
A Helm chart for deploying UnicornTranscoder on Kubernetes with the ability to automatically scale the transcoders as CPU load increases.

Current chart version is `0.1.0`

Source code can be found [here](https://github.com/Unicorn-K8s/UnicornTrancoder-chart)

## Chart Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://github.com/AmitKumarDas/metac/tree/master/helm/metac | MetaC | latest |

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| XPlexToken | string | `nil` | X-Plex-Token for your server See: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/ for guide to find it after creating the server |
| affinity.unicornLoadbalancer | object | `{}` |  |
| affinity.unicornTranscoder | object | `{}` |  |
| claimToken | string | `nil` | Generated token for automatically adding a server under your Plex account See: https://plex.tv/claim to generate one Note: Token is only valid for 4 minutes |
| data.plexConfig.accessMode | string | `"ReadWriteOnce"` |  |
| data.plexConfig.claimName | string | `"plex-config-pvc"` | Name of already existing PVC used to store the configuration data for plex If claimName is defined then the storage class and size are ignored |
| data.plexConfig.size | string | `"60Gi"` | Size of the created PVC If claimName is defined then this is ignored |
| data.plexDB.accessMode | string | `"ReadWriteOnce"` |  |
| data.plexDB.claimName | string | `"plex-db-pvc"` | Name of already existing PVC used as long term storage for the Plex SQLite Database If claimName is defined then the storage class and size are ignored |
| data.plexDB.size | string | `"10Gi"` | Size of the created PVC If claimName is defined then this is ignored |
| data.plexMedia.accessMode | string | `"ReadWriteOnce"` |  |
| data.plexMedia.claimName | string | `"tv-movies-pvc"` | Name of already existing PVC that holds all of the media for Plex If claimName is defined then the storage class and size are ignored |
| data.plexMedia.size | string | `"100Gi"` | Size of the created PVC If claimName is defined then this is ignored |
| data.transcoding.claimName | string | `nil` | Name of already existing PVC to be used by the transcoders to use while transcoding media If claimName is defined then the storage class and size are ignored Claim must be fore a ReadWriteMany PVC |
| data.transcoding.size | string | `"120Gi"` | Size of the created PVC If claimName is defined then this is ignored |
| data.transcoding.storageClass | string | `"hostpath"` | Name of Storage Class to use to create the transcoding PVC |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{"cert-manager.io/cluster-issuer":"letsencrypt-prod","kubernetes.io/ingress.class":"nginx","kubernetes.io/tls-acme":"true","nginx.ingress.kubernetes.io/configuration-snippet":"more_set_input_headers \"Referer: localhost\" ;\nmore_set_input_headers \"Origin: localhost\" ;\n","nginx.ingress.kubernetes.io/proxy-buffering":"off","nginx.ingress.kubernetes.io/proxy-http-version":"1.1","nginx.ingress.kubernetes.io/proxy-redirect-from":"http://localhost$request_uri","nginx.ingress.kubernetes.io/proxy-redirect-to":"$scheme://plex.mydomain.tld$request_uri","nginx.ingress.kubernetes.io/upstream-vhost":"localhost"}` | Any annotations to add to the Plex Ingress |
| ingress.enabled | bool | `true` | Use Kubernetes Ingress to access plex |
| ingress.host | string | `"plex.jeansburger.net"` | Domain name to use for ingress to plex |
| ingress.tls.host | string | `"plex.jeansburger.net"` | Domain name to use on the TLS Certifcate |
| ingress.tls.secretName | string | `"plex-tls"` | Name of secret to hold TLS Certifcate |
| nodeSelector.unicornLoadbalancer | object | `{}` |  |
| nodeSelector.unicornTranscoder | object | `{}` |  |
| plex.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| plex.repository | string | `"plexinc/pms-docker"` | Repository hosting the Plex Media Server image Currently only Official PlexInc image is supported |
| plex.tag | string | `"1.19.1.2645-ccb6eb67e"` | Plex Sever Version Should be set to the current version supported by the UnicornTranscoder Project |
| plexAdvertiseIPs | list | `[]` | List of IPs or FQDNs with ports to be set in the Advertise IPs section of your server |
| plexDBBackup.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| plexDBBackup.repository | string | `"donicrosby/unicorn-plex-sqlite-streamer"` | Repository hosting Unicorn Plex SQLite Streamer image |
| plexDBBackup.tag | string | `"0.1.1"` | SQLite Streamer image tag |
| plexGID | int | `100` | (int) GID to be set for the Plex Server and UnicornTranscoder for accessing media |
| plexHostname | string | `"Unicorn-Plex-K8s"` | Frendly name for your Plex Server |
| plexUID | int | `1000` | (int) UID to be set for the Plex Server and UnicornTranscoder for accessing media |
| podSecurityContext | object | `{}` |  |
| resources.requests.cpu | int | `2` | Number of CPU cores to allocate for the Plex Media Server |
| resources.requests.memory | string | `"2Gi"` | Amount of Memory to allocate for the Plex Media Server |
| resources.unicornLoadbalancer.requests.cpu | string | `"500m"` | Amount of CPU cores to allocate for the Unicorn LoadBalancer |
| resources.unicornLoadbalancer.requests.memory | string | `"500Mi"` | Amount of memory to allocate for the Unicorn Loadbalancer |
| resources.unicornTranscoder.requests.cpu | int | `4` | Amount of CPU cores to allocate for the Unicorn Transcoder |
| resources.unicornTranscoder.requests.memory | string | `"4Gi"` | Amount of memory to allocate for the Unicorn Transcoder |
| securityContext | object | `{}` |  |
| service.advertiseWithService | bool | `false` | Add the LoadBalancer IP and port to the Advertise IPs List |
| service.annotations | object | `{"metallb.universe.tf/allow-shared-ip":"unicorn-plex"}` | Any annotations to be added to the LoadBalancer |
| service.loadbalancerIP | string | `"172.16.4.5"` | IP to be used by the loadbalancer (Recommended to be hardcoded) |
| service.port | int | `3001` | Port to be used for Ingress of the LoadBalancer |
| service.type | string | `"LoadBalancer"` | Service type to be used to expose the UnicornLoadbalancer (and Plex) Currently only LoadBalancer is supported |
| serviceAccount.create | bool | `false` |  |
| serviceAccount.name | string | `nil` |  |
| timezone | string | `"Etc/UTC"` | Timezone to be set for the server See: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for list |
| tolerations.unicornLoadbalancer | list | `[]` |  |
| tolerations.unicornTranscoder | list | `[]` |  |
| transcoding.hpa | bool | `true` | (bool) Determine if chart should deploy a Horizontal Pod Autoscaler for the UnicornTranscoders |
| transcoding.hpaCPUPercent | int | `50` | (int) Percentage of requested CPUs over all UnicornTranscoder Pods for the to be utilized before a new UnicornTranscoder pod is created |
| transcoding.maxReplicas | int | `16` | (int) Maximum number of replicas to be created by the HPA Note: This is ignored if transcoding.hpa is set to false |
| transcoding.port | int | `443` | (int) Port to be used by the created transcoding services |
| transcoding.replicas | int | `4` | (int) Number of replicas to be created by the Transcoder StatefulSet |
| transcoding.transcodeDomain | string | `"plex.mydomain.tld"` |  |
| unicornLoadbalancer.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| unicornLoadbalancer.repository | string | `"donicrosby/unicorn-loadbalancer"` | Repository hosting UnicornLoadbalancer image |
| unicornLoadbalancer.tag | string | `"2.4.3"` | UnicornLoadbalancer version Should be inline with most recent version of UnicornLoadbalancer version |
| unicornTranscoder.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| unicornTranscoder.repository | string | `"donicrosby/unicorn-transcoder"` | Repository hosting UnicornTranscoder image |
| unicornTranscoder.tag | string | `"2.4.2"` | UnicornTranscoder version |

## Deploying this chart

### Prerequisites
In order to use this chart you must have at least the following installed on your cluster:
+ MetaC (A fork of Google Metacontroller Project) found [here](https://github.com/AmitKumarDas/metac/tree/master/helm/metac)
+ Favorite flavor of Ingress controller installed (This project currently uses Ingress Nginx)
+ Have CertBot or another ACME Protocol operator to generate TLS certificates
+ MetalLB if this a baremetal installation the current chart for it can be found [here](https://github.com/helm/charts/tree/master/stable/metallb)
+ Have a plex claim token for the account you are adding the server to (Get one from https://plex.tv/claim)

### Installation
+ Go into the values.yaml and using the Values section above an update to your configuration (be sure to update the ingress.annotations proxy-redirect-to value to your domain)
+ Verify that the plex server/loadbalancer pod is running
+ Verify you can access your Plex Server externally from the domain you used for Ingress
+ Follow the guide [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) in order find you X-Plex-Token update your values.yaml to use the new X-Plex-Token
+ Perform a helm update with your new values.yaml in order to deploy the X-Plex-Token secret for your Transcoders (You may need to wipe them out in order get the token to be updated)
+ Verify you can play a video from the Plex server

If you have any issues please use open an issue so one of the chart maintainers can help you debug it

### External/Extra Configuration
#### Reverse Proxy Setup/Configuration
If you have a reverse proxy on your router (or your router is set to port forward 80/443 to one) you need to accept and proxy these domains to your Plex K8s Cluster:
+ plex.yourdomain.tld
+ *project-name*-transcoder-*number*.yourtranscodedomain.tld

If your plex domain is the same as your transcode domain you can use the following regex:
(?:.+\.)?plex.yourdomain.tld
