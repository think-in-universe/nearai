import os

# API URLs
CLOUD_API_URL = os.getenv('CLOUD_API_URL', 'https://cloud-api.phala.network')
CLOUD_URL = os.getenv('CLOUD_URL', 'https://cloud.phala.network')

# Docker Hub API
DOCKER_HUB_API_URL = 'https://hub.docker.com/v2'

# TEE Simulator
TEE_SIMULATOR = 'phalanetwork/tappd-simulator:latest'

# Default resource configurations
DEFAULT_VCPU = 2
DEFAULT_MEMORY = 4096  # MB
DEFAULT_DISK_SIZE = 40  # GB

# Default TEEPod ID
DEFAULT_TEEPOD_ID = '3'
DEFAULT_IMAGE = 'dstack-0.3.5'

# API Endpoints
class API_ENDPOINTS:
    # Auth
    USER_INFO = '/api/v1/auth/me'

    # TEEPods
    TEEPODS = '/api/v1/teepods/available'
    
    @staticmethod
    def TEEPOD_IMAGES(teepod_id: str) -> str:
        return f'/api/v1/teepods/{teepod_id}/images'
    
    # CVMs
    @staticmethod
    def CVMS(user_id: int) -> str:
        return f'/api/v1/cvms?user_id={user_id}'
    
    @staticmethod
    def CVM_BY_APP_ID(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}'
    
    @staticmethod
    def CVM_NETWORK(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/network'
    
    @staticmethod
    def CVM_START(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/start'
    
    @staticmethod
    def CVM_STOP(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/stop'
    
    @staticmethod
    def CVM_RESTART(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/restart'
    
    @staticmethod
    def CVM_LOGS(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/logs'
    
    CVM_FROM_CONFIGURATION = '/api/v1/cvms/from_cvm_configuration'
    CVM_PUBKEY = '/api/v1/cvms/pubkey/from_cvm_configuration'
    
    @staticmethod
    def CVM_UPGRADE(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/compose'
    
    @staticmethod
    def CVM_ATTESTATION(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/attestation'
    
    @staticmethod
    def CVM_RESIZE(app_id: str) -> str:
        return f'/api/v1/cvms/app_{app_id}/resources'
