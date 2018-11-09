HEADER_ONLY = False

FILENAME_CONVENTION = "camel"

LICENSE = """
"""

HDR_TEMPLATE = """
#ifndef ${IFDEF_GUARD}
#define ${IFDEF_GUARD}
${NAMESPACE_OPEN}
class ${CLASS_NAME}
{
public:
  ${CLASS_NAME}();

private:
};
${NAMESPACE_CLOSE}
#endif // ${IFDEF_GUARD}
"""

SRC_TEMPLATE = """
#include "${HEADER_FILE}"
${NAMESPACE_OPEN}
${CLASS_NAME}::${CLASS_NAME}()
{
}
${NAMESPACE_CLOSE}
"""

