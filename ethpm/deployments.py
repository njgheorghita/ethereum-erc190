class Deployments:
    deployment_data = None
    contract = None

    def __init__(self, deployment_data, w3):
        self.deployment_data = deployment_data
        self.w3 = w3
