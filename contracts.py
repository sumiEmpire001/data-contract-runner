"""Validate CSV records against a declarative JSON data contract."""
import argparse
import csv
import json
import re


def validate_contract(contract):
    if not isinstance(contract,dict) or not isinstance(contract.get("fields"),list) or not contract["fields"]:
        raise ValueError("contract needs fields")
    names=set()
    for field in contract["fields"]:
        name=field.get("name")
        if not isinstance(name,str) or not name or name in names or field.get("type") not in ("string","integer","number","boolean"):
            raise ValueError("invalid or duplicate field")
        names.add(name)
    return contract


def validate_value(value,field):
    if field.get("required",False) and value=="":
        return "required"
    if value=="":
        return None
    kind=field["type"]
    if kind=="integer" and not re.fullmatch(r"[+-]?\d+",value):
        return "not an integer"
    if kind=="number":
        try:
            import math
            if not math.isfinite(float(value)): return "not a finite number"
        except ValueError:
            return "not a number"
    if kind=="boolean" and value.lower() not in ("true","false","1","0"):
        return "not a boolean"
    if "allowed" in field and value not in field["allowed"]:
        return "not in allowed values"
    return None


def check(rows,contract):
    validate_contract(contract)
    errors=[]
    count=0
    for rownum,row in enumerate(rows,start=2):
        count+=1
        for field in contract["fields"]:
            name=field["name"]
            value=row.get(name)
            if value is None:
                errors.append({"row":rownum,"field":name,"reason":"missing column"})
                continue
            reason=validate_value(value,field)
            if reason:
                errors.append({"row":rownum,"field":name,"reason":reason})
    return {"rows":count,"valid":not errors,"errors":errors}


def run(csv_file,contract_file):
    with open(contract_file,encoding="utf-8") as source:
        contract=json.load(source)
    with open(csv_file,newline="",encoding="utf-8") as source:
        return check(csv.DictReader(source),contract)


def main():
    parser=argparse.ArgumentParser(description="Check CSV data against JSON contract")
    parser.add_argument("csv_file")
    parser.add_argument("contract_file")
    args=parser.parse_args()
    report=run(args.csv_file,args.contract_file)
    print(json.dumps(report,indent=2))
    return 0 if report["valid"] else 1


if __name__=="__main__":
    raise SystemExit(main())
