WORKDIR="$( cd "$( dirname "$0"  )" && pwd  )"
docker run --rm -v ${WORKDIR}:/workspace/SEU-health-reporting-helper shrh:0.1 python3 main.py