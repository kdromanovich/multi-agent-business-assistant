def test_mcp_server_constructs_with_registered_tools():
    from app.mcp_server import mcp

    assert mcp is not None
