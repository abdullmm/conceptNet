# use conceptnet

import json
import requests

d3graph = {'nodes' : [], 'links' : []}
theword= 'person'
def recurseCN(id, con, rel ,level, limit, direction):


    # set up node for graph
    d3node = {'id': con['@id'], 'label' : con['@id'].replace('/c/en/', ''), 'type' : 'startnode' if con['@id'].replace('/c/en/', '') == theword else 'plainnode'}
    if d3node not in d3graph['nodes']:
        d3graph['nodes'].append(d3node)



    
    # check for stopping condition
    if level == limit:
        return
    if 'edges' not in con.keys():
        return
    
    # setting up indent string
    indent = ''
    for i in range(0,level):
        indent += '  --'

    # looping through edges 
    for edge in con['edges']:
        if edge['rel']['label'] in rel:
            id2=''
            # print a line and getting id of next concept
            if(direction=='forward' and edge['start']['@id']==id and edge['end']['language']=='en'):
                print(indent,edge['start']['label'], edge['rel']['label'], edge['end']['label'])
                id2=edge['end']['@id']
            if(direction=='backward' and edge['end']['@id']==id and edge['start']['language']=='en'):
                print(indent,edge['start']['label'], edge['rel']['label'], edge['end']['label'])
                id2 = edge['start']['@id']
            # request next concept from ConceptNet
            if id2!='':
                con2= requests.get('http://api.conceptnet.io' + id2).json()

                # add link to graph
                d3link = {'source' : edge['start']['@id'], 'target' : edge['end']['@id'], 'type' : edge['rel']['label']}
                if d3link not in d3graph['links']:
                    d3graph['links'].append(d3link)
                
                # recurse
                recurseCN(id2,con2,rel ,level+1,limit,direction)
        


#get initial concepts from ConceptNet

concept = requests.get('http://api.conceptnet.io/c/en/' + theword).json()


print('Processing concept:', concept['@id'])

# traverse forward
print("FORWARD")
recurseCN(concept['@id'], concept, ['IsA', 'PartOf', 'UsedFor', 'RelatedTo', 'CapableOf', 'MotivatedByGoal', 'Desires', 'AtLocation'] , 0, 2, 'forward')
print()

# traverse backward
print("BACKWARD")
recurseCN(concept['@id'], concept, ['IsA', 'PartOf', 'UsedFor', 'RelatedTo', 'CapableOf', 'MotivatedByGoal', 'Desires', 'AtLocation'] , 0, 2, 'backward')
print()

