# Bilibili API URL （非官方公布）
# -Videos-
# --Common videos--
get_cid_API=r"https://api.bilibili.com/x/player/pagelist"
'''
(aid 与 bvid 任选一个)
aid: num *
bvid: str *
'''
get_streamURL_API=r"https://api.bilibili.com/x/player/playurl"
'''
(aid 与 bvid 任选一个)
aid: num *
bvid: str *
cid: num *
qn: num
fnval: num
fourk: num (1 or 0)
'''
# --bangumi and movies
bangumi_get_cid_API=r"https://api.bilibili.com/pgc/view/web/season" #GET
'''
(season_id 与 ep_id 任选一个)
season_id: num *
ep_id: num *
'''
bangumi_get_StreamURL=r"https://api.bilibili.com/pgc/player/web/playurl" #GET
'''
(ep_id 与 cid 任选一个)
ep_id: num *
cid: num *
qn: num
fnval: num
fourk: num (0 or 1)
'''