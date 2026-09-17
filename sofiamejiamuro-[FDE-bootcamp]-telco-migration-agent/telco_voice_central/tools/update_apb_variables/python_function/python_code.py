def update_apb_variables(department_id: str = "", cirn: float = 0.0, clid: float = 0.0) -> dict:
    '''Generates department_id_ref and conditionally manages cirn based on clid.'''
    if get_variable("mock_mode"):
        mock_dep_id = str(department_id).strip() if department_id else "9999"
        return {
            "status": "success",
            "department_id_ref": f"REF{mock_dep_id}"
        }
    else:
        try:
            sanitized_dep_id = str(department_id).strip()
            dept_id_ref = f"REF{sanitized_dep_id}" if sanitized_dep_id else "REF"
            set_variable("department_id_ref", dept_id_ref)
            print("Business logic success - department_id_ref set.")

            current_cirn = get_variable("cirn")
            if not current_cirn or current_cirn == 0.0:
                current_clid = get_variable("clid")
                fallback_clid = current_clid if current_clid else clid
                set_variable("cirn", fallback_clid)
                print("Business logic success - cirn updated with clid.")

            return {"status": "success", "department_id_ref": dept_id_ref}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer of technical difficulties and transition to an agent."}