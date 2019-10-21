import requests


def get_ecs_task_ips():
    """
    Retrieve the internal ip address(es) for task, if running with AWS ECS and awsvpc networking mode
    Used to get ips to add to ALLOWED_HOSTS setting, for load balancer health checks
    See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint.html
    Uses V2 endpoint: http://169.254.170.2/v2/metadata
    :return: list of internal ip addresses
    """
    ip_addresses = []
    try:
        r = requests.get("http://169.254.170.2/v2/metadata", timeout=0.01)
    except requests.exceptions.RequestException:
        return []
    if r.ok:
        task_metadata = r.json()
        for container in task_metadata['Containers']:
            for network in container['Networks']:
                if network['NetworkMode'] == 'awsvpc':
                    ip_addresses.extend(network['IPv4Addresses'])
    return list(set(ip_addresses))


def get_ec2_instance_ips():
    """
    Retrieve the private ip address(es) for EC2 instance.
    Used to get ips to add to ALLOWED_HOSTS setting, for load balancer health checks.
    See https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    :return: list of internal ip addresses
    """
    ip_addresses = []
    try:
        r = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4", timeout=0.01)
    except requests.exceptions.RequestException:
        pass
    if r.ok:
        ip_addresses.append(r.text)
    return ip_addresses
