import os
from fastmcp import FastMCP
from dotenv import load_dotenv
from pypco import PCO

load_dotenv()

mcp = FastMCP("Planning Center Demo")
pco = PCO(os.environ.get("PCO_CLIENT_ID"), os.environ.get("PCO_SECRET"))

@mcp.tool
def lookup_pco_service_types() -> list[dict[str, str]]:
    """Look up service types from Planning Center Online."""
    service_types = pco.get("/services/v2/service_types")

    output = []

    for service_type in service_types["data"]:

        row = {
            "id": service_type["id"],
            "name": service_type["attributes"]["name"]
        }

        output.append(row)

    return output

def lookup_pco_next_service(service_type_id: int) -> int:
    """Gets the id for the next service in Planning Center Online."""

    next_plan = next(pco.iterate(f"/services/v2/service_types/{service_type_id}/plans", filter="future", per_page=1, sort="sort_date"))

    return int(next_plan["data"]["id"])

@mcp.tool
def get_pco_next_service_order_items(service_type_id: int) -> list[dict[str, str]]:
    """Gets the order items for the next service in Planning Center Online."""

    next_service_id = lookup_pco_next_service(service_type_id)

    order_items = pco.get(f"/services/v2/service_types/{service_type_id}/plans/{next_service_id}/items")

    output = []

    for item in order_items["data"]:

        row = {
            "id": item["id"],
            "title": item["attributes"]["title"],
            "item_type": item["attributes"]["item_type"],
        }

        output.append(row)

    return output

if __name__ == "__main__":
    mcp.run()