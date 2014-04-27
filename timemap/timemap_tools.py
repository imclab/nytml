# traverse all comments
def traverse_all():
    gc.enable() # garbage collector
    s, e, idmap = MIN_DATE, MAX_DATE, {}
    s_y, fail_count = s.year, 0

    with open('id_timemap.json', 'r') as g: idmap = json.load(g)
    print 'id map loaded'

    while cmp(s, e) != 0:
        if s_y != s.year:
            print s_y # track progress
            s_y = s.year
            gc.collect()

        comments = get_comment_list(s)

        if len(comments) == 0:
            s = incrementDate(s)
            continue

        for comment in comments:
            id = comment['commentID']
            if str(id) in idmap:
                timeRank, elapsed = idmap[str(id)]
                comment['timeRank'] = timeRank
                comment['elapsedTime'] = elapsed
            else:
                print 'failed on ', id

        write_comment_list(s, comments)
        s = incrementDate(s)
        print s

def processURLTimeMap():

    urlmap, id_timemap, tdiff, first = {}, {}, 0, 0

    with open('url_timemap.json', 'r') as f:
        urlmap = json.load(f)
        
    print 'Finished loading url time-map'

    if urlmap:
        
        for url in urlmap.keys():
            
            id_time_list = urlmap[url]
            ranked = sorted(id_time_list, key=lambda x: int(x[1]))
            
            for i in range(len(ranked)):

                val = ranked[i]
                c_id, c_rank = val[0], i

                if i > 0: tdiff = int(val[1]) - first
                else: tdiff, first = 0, int(val[1])
                
                id_timemap[c_id] = (c_rank, tdiff)
            
            print 'done ', url

    with open('id_timemap.json', 'w+') as g: json.dump(id_timemap, g)