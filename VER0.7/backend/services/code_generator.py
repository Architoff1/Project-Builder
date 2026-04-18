import requests
import re

MISTRAL_API_URL = "https://unsetting-chelsea-unturbidly.ngrok-free.dev/generate"


def clean_code(code, file_name):
    code = code.strip()

    code = code.replace("```", "").strip()

    code = re.sub(r"^(html|css|javascript|js|python|json)\s*", "", code, flags=re.IGNORECASE)

    code = re.sub(r"^.*?(<!DOCTYPE|<html|body\s*\{|document\.|def |function |{)", r"\1", code, flags=re.DOTALL)

    if file_name.endswith(".html"):
        if "<!DOCTYPE" in code:
            code = code[code.index("<!DOCTYPE"):]
        elif "<html" in code:
            code = code[code.index("<html"):]
    elif file_name.endswith(".js"):
        match = re.search(r"(document\.|window\.|function|const|let|var)", code)
        if match:
            code = code[match.start():]
    elif file_name.endswith(".py"):
        match = re.search(r"(def |import |from )", code)
        if match:
            code = code[match.start():]
    elif file_name.endswith(".json"):
        match = re.search(r"\{", code)
        if match:
            code = code[match.start():]

    return code.strip()


def get_fallback(file_name):
    if file_name.endswith(".html"):
        return "<!DOCTYPE html><html><body><h3>⚠️ Code generation failed</h3></body></html>"
    elif file_name.endswith(".css"):
        return "/* Code generation failed */"
    elif file_name.endswith(".js"):
        return "// Code generation failed"
    elif file_name.endswith(".py"):
        return "# Code generation failed"
    elif file_name.endswith(".json"):
        return "{}"
    else:
        return "// Code generation failed"


def build_related_summary(current_file, files):
    related_files = [f for f in files if f != current_file]

    summary = ""
    for rf in related_files:
        summary += f"- {rf}\n"

    return summary

def validate_code(file, code):
    issues = []

    if file.endswith(".js"):
        if "querySelectorAll" in code and "forEach" in code and "numbers" not in code:
            issues.append("Missing variable declaration for selected elements")

        if "getElementById('equal')" in code and "id=\"equal\"" not in code:
            issues.append("JS references 'equal' but HTML may not contain it")

    if file.endswith(".css"):
        if code.strip().startswith("{"):
            issues.append("CSS missing selector before block")

    return issues

def generate_code(files, steps, context):
    code_map = {}

    for file in files:
        print(f"\n🔧 Generating file: {file}")

        # 🔥 Build dependency context
        related_summary = build_related_summary(file, files)

        prompt = f"""
        You are an expert software developer.

        PROJECT PLAN:
            {steps}

        PROJECT FILES:
            {files}

        CURRENT FILE:
            {file}

        RELATED FILES:
            {related_summary}

        ────────────────────────
        SYSTEM UNDERSTANDING
        ────────────────────────
            - First, understand the type of project (web app, backend, CLI tool, ML system, etc.)
            - Determine the role of this file within the overall system
            - Generate code appropriate to the system and file responsibility

        ────────────────────────
        SYSTEM RULES
        ────────────────────────
            - All files must work together as ONE complete system
            - Maintain consistency across files (imports, APIs, UI, logic, naming)
            - Respect relationships and dependencies between files
            - Do NOT invent unrelated components or architecture

        ────────────────────────
        STRUCTURE RULES
        ────────────────────────
            - Distribute logic appropriately across files
            - Do NOT split a single logical component unnecessarily
            - Do NOT create placeholder files or incomplete components
            - Every file must contribute meaningfully to the system

        ────────────────────────
        CONSISTENCY RULES
        ────────────────────────
            - If this file references something → it MUST exist in another file
            - If other files depend on this file → ensure compatibility
            - Naming, variables, APIs, and structures must align across files

        ────────────────────────
        ENGINEERING MODE
        ────────────────────────
            - Build a COMPLETE, FUNCTIONAL, and CLEAN solution
            - Use best practices where appropriate
            - Prefer clarity, correctness, and maintainability

        ────────────────────────
        INTELLIGENCE CONTROL
        ────────────────────────
            - You have full knowledge of software engineering across domains
            - Decide how much complexity and which techniques to apply based on the task

        MODE SELECTION:
            - Simple task → minimal and direct implementation
            - Moderate task → structured and clean design
            - Complex system → scalable and well-organized architecture

        ────────────────────────
        COMPLEXITY CONTROL
        ────────────────────────
            - Match complexity to the problem
            - Do NOT over-engineer
            - Do NOT introduce unnecessary frameworks, layers, or tools
            - Do NOT add backend, APIs, or extra systems unless required

        ────────────────────────
        INTENT ALIGNMENT
        ────────────────────────
            - Follow the user's request strictly
            - You may improve usability, clarity, and correctness
            - BUT you must NOT expand or change the core scope

        ────────────────────────
        CRITICAL RULES
        ────────────────────────
            - Do NOT leave placeholders (e.g., "to be implemented", "UI goes here")
            - Do NOT generate incomplete logic
            - Do NOT assume files that are not listed
            - Ensure the code is logically runnable and complete

        ────────────────────────
        OUTPUT RULES
        ────────────────────────
            - Output ONLY code
            - No explanations
            - No markdown
            - No extra text

        Generate code for THIS file only.
        """

        try:
            response = requests.post(
                MISTRAL_API_URL,
                json={"prompt": prompt},
                timeout=120
            )

            response.raise_for_status()
            result = response.json()

            raw_code = result.get("response", "") or ""

            print(f"📦 RAW OUTPUT:\n{raw_code[:200]}\n")

            if not raw_code:
                code_map[file] = get_fallback(file)
                continue

            code = clean_code(raw_code, file)
            issues = validate_code(file, code)
            
            if issues:
                print(f"⚠️ Issues found in {file}: {issues}")
            
                fix_prompt = f"""
                You are an expert software developer fixing broken code.
                ORIGINAL CODE:
                    {code}
                    
                DETECTED ISSUES:
                    {issues}

                PROJECT CONTEXT:
                    - This file is part of a multi-file system
                    - It must work correctly with other related files

                RELATED FILES:
                    {related_summary}

                ────────────────────────
                FIXING RULES
                ────────────────────────
                    - Fix ALL issues while preserving the intended functionality
                    - Ensure all variables, functions, and references are properly defined
                    - Ensure all referenced elements, modules, or dependencies exist
                    - Ensure consistency with related files

                ────────────────────────
                SYSTEM CONSISTENCY
                ────────────────────────
                    - Do NOT introduce new architecture or unrelated logic
                    - Do NOT change the purpose of the file
                    - Maintain compatibility with other files
                    - Follow naming and structure consistency

                ────────────────────────
                COMPLETENESS
                ────────────────────────
                    - Do NOT leave placeholders
                    - Do NOT leave partial implementations
                    - Ensure the code is logically complete and runnable

                ────────────────────────
                OUTPUT RULES
                ────────────────────────
                    - Return ONLY corrected code
                    - No explanations
                    - No markdown
                """
                
                fix_response = requests.post(MISTRAL_API_URL,json={"prompt": fix_prompt},timeout=120)
                
                fixed = fix_response.json().get("response", "")
                code = clean_code(fixed, file)
            
            print(f"🧹 CLEANED OUTPUT:\n{code[:200]}\n")

            if not code or len(code) < 5:
                code = get_fallback(file)

            code_map[file] = code

        except Exception as e:
            print(f"❌ Error generating code for {file}: {e}")
            code_map[file] = get_fallback(file)

    return code_map