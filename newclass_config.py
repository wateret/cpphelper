HEADER_ONLY = False

FILENAME_CONVENTION = "camel"

LICENSE = """
/*
 * Copyright (c) 2018 Samsung Electronics Co., Ltd. All Rights Reserved
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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

