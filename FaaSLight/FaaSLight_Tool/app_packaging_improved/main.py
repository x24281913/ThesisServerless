import packaging
from packaging import version
from packaging import specifiers
from packaging import requirements
from packaging import markers
from packaging import tags
from packaging import utils
from packaging.version import Version
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement
from packaging.markers import Marker

def lambda_handler(event, context):
    ver_str = event.get('version', '1.2.3')
    spec_str = event.get('specifier', '>=1.0.0')
    req_str = event.get('requirement', 'requests>=2.0.0')
    v = Version(ver_str)
    spec = SpecifierSet(spec_str)
    req = Requirement(req_str)
    marker = Marker("python_version >= '3.6'")
    return {'statusCode': 200, 'body': {'version': str(v), 'matches_spec': ver_str in spec, 'requirement': str(req), 'marker_evaluated': marker.evaluate()}}

