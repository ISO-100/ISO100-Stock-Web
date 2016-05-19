from MySQLdb import cursors
from flask import request

class DataTablesServer(object):
 
    def __init__( self, request, columns, index, table, cursor):
        self.columns = columns
        self.index = index
        self.table = table
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
         
        # pass MysqlDB cursor
        self.dbh = cursor
 
        # results from the db
        self.resultData = None
         
        # total in the table after filtering
        self.cadinalityFiltered = 0
 
        # total in the table unfiltered
        self.cadinality = 0
 
        self.run_queries()
 
 
    def output_result(self):
        # return output
        output = {}
        output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.cardinality)
        output['iTotalDisplayRecords'] = str(self.cadinalityFiltered)
        aaData_rows = []
 
        for row in self.resultData:
            aaData_row = []
            for i in range( len(self.columns) ):
                aaData_row.append(str(row[ self.columns[i] ]).replace('"','\\"'))
             
            # add additional rows here that are not represented in the database
            # aaData_row.append(('''<input id='%s' type='checkbox'></input>''' % (str(row[ self.index ]))).replace('\\', ''))
 
            aaData_rows.append(aaData_row)
 
        output['aaData'] = aaData_rows 
        return output
 
    def run_queries(self):
        dataCursor = self.dbh(cursors.DictCursor) # replace the standard cursor with a dictionary cursor only for this query
        dataCursor.execute( """
            SELECT SQL_CALC_FOUND_ROWS %(columns)s
            FROM   %(table)s %(where)s %(order)s %(limit)s""" % dict(
                columns=', '.join(self.columns), table=self.table, where=self.filtering(), order=self.ordering(),
                limit=self.paging()
            ) )
        self.resultData = dataCursor.fetchall()

        cadinalityFilteredCursor = self.dbh.cursor()
        cadinalityFilteredCursor.execute( """
            SELECT FOUND_ROWS()
        """ )
        self.cadinalityFiltered = cadinalityFilteredCursor.fetchone()[0]

        cadinalityCursor = self.dbh.cursor()
        cadinalityCursor.execute( """SELECT COUNT(%s) FROM %s""" % (self.index, self.table))
        self.cardinality = cadinalityCursor.fetchone()[0]

 
    def filtering(self):         
        # build your filter spec

        filter = ""
        if ( self.request_values.has_key('sSearch') ) and ( self.request_values['sSearch'] != "" ):
            filter = "WHERE "
            for i in range( len(self.columns) ):
                filter += "%s LIKE '%%%s%%' OR " % (self.columns[i], self.request_values['sSearch'])
            filter = filter[:-3]
        return filter
        
        # individual column filtering if needed
        
        #and_filter_individual_columns = []
        #for i in range(len(columns)):
        #    if (request_values.has_key('sSearch_%d' % i) and request_values['sSearch_%d' % i] != ''):
        #        individual_column_filter = {}
        #        individual_column_filter[columns[i]] = {'$regex': request_values['sSearch_%d' % i], '$options': 'i'}
        #        and_filter_individual_columns.append(individual_column_filter)
 
        #if and_filter_individual_columns:
        #    filter['$and'] = and_filter_individual_columns
        #return filter

    def ordering( self ):
        order = ""
        if ( self.request_values['iSortCol_0'] != "" ) and ( self.request_values['iSortingCols'] > 0 ):
            order = "ORDER BY  "
            for i in range( int(self.request_values['iSortingCols']) ):
                order += "%s %s, " % (self.columns[ int(self.request_values['iSortCol_'+str(i)]) ], \
                    self.request_values['sSortDir_'+str(i)])
        return order[:-2]
 
    def paging(self):
        limit = ""
        if ( self.request_values['iDisplayStart'] != "" ) and ( self.request_values['iDisplayLength'] != -1 ):
            limit = "LIMIT %s, %s" % (self.request_values['iDisplayStart'], self.request_values['iDisplayLength'] )
        return limit