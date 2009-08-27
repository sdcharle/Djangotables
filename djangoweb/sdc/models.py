from django.db import models

# CD record - records describing the CDs in yar collection son.
# text fields be boring but bah, whatareyougonnado?

"""
model weirdness:

sdc.models.CDRecord.objects.filter(artist = 'Magic Fred').delete()
                                           record = sdc.models.CDRecord.objects.create(artist = 'Magic Fred', title = 'beat it off')

In [33]: record.save()

Says:

IntegrityError (IntegrityError: columns Artist, Title are not unique)

BUT a) they are, b) saves it anyway

Note: if you specify (unique ID, it is happy anyhow)

Try: cdid = AutoField?

For fun later:

/Library/Python/2.5/site-packages/django/db/models/base.pyc in save(self, force_insert, force_update)
    309             raise ValueError("Cannot force both insert and updating in "
    310                     "model saving.")
--> 311         self.save_base(force_insert=force_insert, force_update=force_update)
    312 
    313     save.alters_data = True

/Library/Python/2.5/site-packages/django/db/models/base.pyc in save_base(self, raw, cls, force_insert, force_update)
    381             if values:
    382                 # Create a new record.
--> 383                 result = manager._insert(values, return_id=update_pk)
    384             else:
    385                 # Create a new record with defaults for everything.

/Library/Python/2.5/site-packages/django/db/models/manager.pyc in _insert(self, values, **kwargs)
    136 
    137     def _insert(self, values, **kwargs):
--> 138         return insert_query(self.model, values, **kwargs)
    139 
    140     def _update(self, values, **kwargs):

/Library/Python/2.5/site-packages/django/db/models/query.pyc in insert_query(model, values, return_id, raw_values)
    890     part of the public API.
    891     
    892     query = sql.InsertQuery(model, connection)
    893     query.insert_values(values, raw_values)
--> 894     return query.execute_sql(return_id)

/Library/Python/2.5/site-packages/django/db/models/sql/subqueries.pyc in execute_sql(self, return_id)
    307 
    308     def execute_sql(self, return_id=False):
--> 309         cursor = super(InsertQuery, self).execute_sql(None)
    310         if return_id:
    311             return self.connection.ops.last_insert_id(cursor,

/Library/Python/2.5/site-packages/django/db/models/sql/query.pyc in execute_sql(self, result_type)
   1732 
   1733         cursor = self.connection.cursor()
-> 1734         cursor.execute(sql, params)
   1735 
   1736         if not result_type:

/Library/Python/2.5/site-packages/django/db/backends/util.pyc in execute(self, sql, params)
     17         start = time()
     18         try:
---> 19             return self.cursor.execute(sql, params)
     20         finally:
     21             stop = time()

/Library/Python/2.5/site-packages/django/db/backends/sqlite3/base.pyc in execute(self, query, params)
    166     def execute(self, query, params=()):
    167         query = self.convert_query(query, len(params))
--> 168         return Database.Cursor.execute(self, query, params)
    169 
    170     def executemany(self, query, param_list):

N.B. = if you create and then save it tries to insert, but creating actually saved it to the DB. w00t

"""

class CDRecord(models.Model):
  # not AutoField?
    cdid = models.AutoField(null=True, primary_key=True, db_column=u'CDID', blank=True) # Field name made lowercase.
    asin = models.TextField(db_column=u'ASIN', blank=True) # Field name made lowercase. This field type is a guess.
    artist = models.TextField(db_column=u'Artist', blank=True) # Field name made lowercase. This field type is a guess.
    manufacturer = models.TextField(db_column=u'Manufacturer', blank=True) # Field name made lowercase. This field type is a guess.
    upc = models.TextField(db_column=u'UPC', blank=True) # Field name made lowercase. This field type is a guess.
    title = models.TextField(db_column=u'Title', blank=True) # Field name made lowercase. This field type is a guess.
    detailpageurl = models.TextField(db_column=u'DetailPageURL', blank=True) # Field name made lowercase. This field type is a guess.
    
    class Meta:
        db_table = u'CDRecord'
        ordering = ('artist', 'title')
        
    def __unicode__(self):
        return u'%s\t%s' % (self.artist, self.title)
    