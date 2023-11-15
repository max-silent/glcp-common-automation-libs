if [[ "$ClusterUnderTest" == *on-prem* ]]; then
    export HTTPS_PROXY=$(jq -r ".clusterinfo.INPUTENV.HTTPS_PROXY" /configmap/data/infra_clusterinfo.json)
    export HTTP_PROXY=$(jq -r ".clusterinfo.INPUTENV.HTTP_PROXY" /configmap/data/infra_clusterinfo.json)
    export NO_PROXY=$(jq -r ".clusterinfo.INPUTENV.NO_PROXY" /configmap/data/infra_clusterinfo.json)
fi