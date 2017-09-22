import mcp

io = mcp.MCP23017()

io.setup(0, mcp.OUT)
io.setup(1, mcp.OUT)
io.setup(2, mcp.OUT)
io.setup(3, mcp.OUT)

io.setup(8, mcp.IN)
io.setup(9, mcp.IN)
io.setup(10, mcp.IN)
io.setup(11, mcp.IN)

io.output(0, 1)
io.output(0, 0)
