import s3transfer
KB = 1024
MB = KB * KB
GB = MB * KB
ALLOWED_DOWNLOAD_ARGS = ['ChecksumMode', 'VersionId', 'SSECustomerAlgorithm', 'SSECustomerKey', 'SSECustomerKeyMD5', 'RequestPayer', 'ExpectedBucketOwner']
FULL_OBJECT_CHECKSUM_ARGS = ['ChecksumCRC32', 'ChecksumCRC32C', 'ChecksumCRC64NVME', 'ChecksumMD5', 'ChecksumSHA1', 'ChecksumSHA256', 'ChecksumSHA512', 'ChecksumXXHASH3', 'ChecksumXXHASH64', 'ChecksumXXHASH128']
USER_AGENT = f's3transfer/{s3transfer.__version__}'
PROCESS_USER_AGENT = f'{USER_AGENT} processpool'

