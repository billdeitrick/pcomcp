import os
import random
from fastmcp import FastMCP
from dotenv import load_dotenv
from pypco import PCO

load_dotenv()

mcp = FastMCP("Planning Center Demo")
pco = PCO(os.environ.get("PCO_CLIENT_ID"), os.environ.get("PCO_SECRET"))

@mcp.tool
def generate_random_number(min: int = 0, max: int = 100) -> int:
    """Generate a random number between min and max."""

    return random.randint(min, max)

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

def get_next_plan_id(service_type_id):
    """Gets the next plan for a given service type."""

    return next(pco.iterate(f"/services/v2/service_types/{service_type_id}/plans", filter="future", per_page=1, sort="sort_date"))["data"]

@mcp.tool
def lookup_pco_next_service(service_type_id: int) -> dict:
    """Gets information about the next plan from Planning Center Online."""

    next_plan = get_next_plan_id(service_type_id)

    return {
        "id": next_plan["id"],
        "dates": next_plan["attributes"]["dates"],
        "series_title": next_plan["attributes"]["series_title"]
    }

@mcp.tool
def get_pco_next_service_order_items(service_type_id: int) -> list[dict[str, str]]:
    """Gets the order items for the next service in Planning Center Online."""

    next_service_id = get_next_plan_id(service_type_id)["id"]

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