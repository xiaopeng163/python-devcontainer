import asyncio

api_tree = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]}


async def get_nodes(tree, root):
    # to simulate a slow API to get nodes
    await asyncio.sleep(1)
    if root not in tree:
        return []
    return tree[root]


async def bfs(tree, root):
    nodes = await get_nodes(tree, root)
    for node in nodes:
        yield node
        async for n in bfs(tree, node):
            yield n


visited = []


async def main():
    async def consumer(generator):
        async for node in generator:
            visited.append(node)

    async_generators = [bfs(tree, "A") for tree in [api_tree] * 10]
    await asyncio.gather(*[consumer(generator) for generator in async_generators])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(visited)
