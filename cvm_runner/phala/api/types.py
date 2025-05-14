from typing import Dict, List, Optional, Any, TypedDict, Union
from dataclasses import dataclass
from decimal import Decimal

class DockerConfig(TypedDict, total=False):
    """Docker configuration"""
    password: str
    registry: Optional[str]
    username: str

class ComposeFile(TypedDict, total=False):
    """Docker compose file configuration"""
    docker_compose_file: str
    docker_config: Optional[DockerConfig]
    features: List[str]
    kms_enabled: bool
    manifest_version: int
    name: str
    public_logs: bool
    public_sysinfo: bool
    runner: Optional[str]
    salt: Optional[str]
    tproxy_enabled: bool
    version: Optional[str]

class Configuration(TypedDict, total=False):
    """VM configuration"""
    name: str
    image: str
    compose_file: ComposeFile
    vcpu: int
    memory: int
    disk_size: int
    ports: List[Any]

class Hosted(TypedDict, total=False):
    """Hosted CVM information"""
    id: str
    name: str
    status: str
    uptime: str
    app_url: str
    app_id: str
    instance_id: str
    configuration: Configuration
    exited_at: str
    boot_progress: str
    boot_error: str
    shutdown_progress: str
    image_version: str

class ManagedUser(TypedDict, total=False):
    """Managed user information"""
    id: int
    username: str

class Node(TypedDict, total=False):
    """Node information"""
    id: int
    name: str

class CvmInstance(TypedDict, total=False):
    """Represents a CVM instance"""
    hosted: Hosted
    name: str
    managed_user: ManagedUser
    node: Node
    listed: bool
    status: str
    in_progress: bool
    dapp_dashboard_url: Optional[str]
    syslog_endpoint: str
    allow_upgrade: bool
    project_id: str
    project_type: Optional[str]
    billing_period: Optional[str]

class PostCvmResponse(TypedDict, total=False):
    """Response for CVM operations"""
    id: int
    name: str
    status: str
    teepod_id: Optional[int]
    teepod: Optional[Dict[str, Any]]
    user_id: int
    app_id: str
    vm_uuid: Optional[str]
    instance_id: Optional[str]
    app_url: Optional[str]
    base_image: str
    vcpu: int
    memory: int
    disk_size: int
    manifest_version: int
    version: str
    runner: str
    docker_compose_file: str
    features: Optional[List[str]]
    created_at: str
    encrypted_env_pubkey: str

class GetPubkeyFromCvmResponse(TypedDict, total=False):
    """Response for getting public key from CVM"""
    app_env_encrypt_pubkey: str
    app_id_salt: str

class GetCvmByAppIdResponse(TypedDict, total=False):
    """Response for getting a CVM by App ID"""
    id: int
    teepod_id: Optional[int]
    teepod: Optional[Dict[str, Any]]
    name: str
    status: str
    in_progress: bool
    app_id: str
    vm_uuid: str
    instance_id: str
    vcpu: int
    memory: int
    disk_size: int
    base_image: str
    encrypted_env_pubkey: str
    listed: bool
    project_id: str
    project_type: Optional[str]

class GetUserInfoResponse(TypedDict, total=False):
    """Response for getting user information"""
    username: str
    email: str
    credits: Decimal
    granted_credits: Decimal
    role: str
    avatar: str
    flag_reset_password: bool
    team_name: str
    team_tier: str
    trial_ended_at: Optional[str]

class UpgradeCvmResponse(TypedDict, total=False):
    """Response for CVM upgrade operation"""
    detail: str

class EncryptedEnvItem(TypedDict, total=False):
    """Encrypted environment variable"""
    key: str
    value: str

class Image(TypedDict, total=False):
    """TEEPod image information"""
    name: str
    description: Optional[str]
    version: Optional[List[int]]
    is_dev: Optional[bool]
    rootfs_hash: Optional[str]
    shared_ro: Optional[bool]
    cmdline: Optional[str]
    kernel: Optional[str]
    initrd: Optional[str]
    hda: Optional[str]
    rootfs: Optional[str]
    bios: Optional[str]

class TEEPod(TypedDict, total=False):
    """TEEPod information"""
    teepod_id: Optional[int]
    name: str
    listed: bool
    resource_score: int
    remaining_vcpu: int
    remaining_memory: int
    remaining_cvm_slots: int
    images: Optional[List[Image]]

class Capacity(TypedDict, total=False):
    """Resource capacity information"""
    max_instances: Optional[int]
    max_vcpu: Optional[int]
    max_memory: Optional[int]
    max_disk: Optional[int]

class TeepodResponse(TypedDict, total=False):
    """Response for TEEPod operations"""
    tier: str
    capacity: Capacity
    nodes: List[TEEPod]

class CvmAttestationResponse(TypedDict, total=False):
    """Response for CVM attestation"""
    attestation: str

class GetCvmNetworkResponse(TypedDict, total=False):
    """Response for CVM network information"""
    is_online: bool
    is_public: bool
    error: Optional[str]
    internal_ip: str
    latest_handshake: str
    public_urls: List[Dict[str, str]]

class VMConfig(TypedDict, total=False):
    """VM configuration type"""
    pass

class UpdateCvmPayload(TypedDict, total=False):
    """Update payload type"""
    app_id: str

class ResizeCvmPayload(TypedDict, total=False):
    """Resize CVM payload type"""
    vcpu: Optional[int]
    memory: Optional[int]
    disk_size: Optional[int]
    allow_restart: Optional[int]

class CertificateNameInfo(TypedDict, total=False):
    """Certificate naming information"""
    common_name: Optional[str]
    organization: Optional[str]
    country: Optional[str]
    state: Optional[str]

class CertificateInfo(TypedDict, total=False):
    """Certificate information"""
    subject: CertificateNameInfo
    issuer: CertificateNameInfo
    serial_number: str
    not_before: str
    not_after: str
    version: str
    fingerprint: str
    signature_algorithm: str
    sans: Optional[str]
    is_ca: bool
    position_in_chain: int
    quote: Optional[str]

class TCBEventLogEntry(TypedDict, total=False):
    """TCB event log entry"""
    imr: int
    event_type: int
    digest: str
    event: str
    event_payload: str

class TCBInfo(TypedDict, total=False):
    """TCB information"""
    mrtd: str
    rootfs_hash: str
    rtmr0: str
    rtmr1: str
    rtmr2: str
    rtmr3: str
    event_log: List[TCBEventLogEntry] 