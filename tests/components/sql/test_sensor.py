"""The test for the sql sensor platform."""
import pytest
import voluptuous as vol

from homeassistant.components.sql.sensor import validate_sql_select
from homeassistant.const import STATE_UNKNOWN
from homeassistant.setup import async_setup_component


async def test_query(hass):
    """Test the SQL sensor."""
    config = {
        "sensor": {
            "platform": "sql",
            "db_url": "sqlite://",
            "queries": [
                {
                    "name": "count_tables",
                    "query": "SELECT 5 as value",
                    "column": "value",
                }
            ],
        }
    }

    assert await async_setup_component(hass, "sensor", config)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.count_tables")
    assert state.state == "5"
    assert state.attributes["value"] == 5


async def test_invalid_query(hass):
    """Test the SQL sensor for invalid queries."""
    with pytest.raises(vol.Invalid):
        validate_sql_select("DROP TABLE *")

    config = {
        "sensor": {
            "platform": "sql",
            "db_url": "sqlite://",
            "queries": [
                {
                    "name": "count_tables",
                    "query": "SELECT * value FROM sqlite_master;",
                    "column": "value",
                }
            ],
        }
    }

    assert await async_setup_component(hass, "sensor", config)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.count_tables")
    assert state.state == STATE_UNKNOWN
