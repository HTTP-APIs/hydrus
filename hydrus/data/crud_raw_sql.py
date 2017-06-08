## To be implemented

1. Query_get = " select classes.name, instances.name, instance_props.name, terminals.value from ((((graph inner join classes on graph.class_ = classes.id) inner join instances on graph.instance = instances.id) inner join instance_props on graph.inst_predicate = instance_props.id) inner join terminals on graph.term_object = terminals.id) where graph.instance=1;"

2. Query_delete steps
1. Get terminal ids from graph
2. Delete terminal objects
3. Delete graph record
4 Delete instance record
