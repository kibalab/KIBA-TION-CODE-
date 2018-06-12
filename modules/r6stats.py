import asyncio
import r6sapi as api


@asyncio.coroutine
def run(name):
    auth = api.Auth("tylerabbottthss@gmail.com", "Chandra66")
    player = yield from auth.get_player(name, api.Platforms.UPLAY)
    A = yield from player.get_rank("apac", season=-1)
    mmr = A.mmr
    print(A.GameQueue)

def start(name):
    return(asyncio.get_event_loop().run_until_complete(run(name)))

start('KIBA_NA')