from django.http import HttpResponse
from django.shortcuts import render_to_response
from djangoweb.sdc.models import CDRecord
import simplejson
import logging
"""
Example View for Datatables jQuery plugin

iDisplayStart - ind to start at
iDisplayLength - how many to show.

iSortingCols (how man cols for sortin)
  iSortCol_i (ith sorting col - zero based)
  iSortDir_i (ith sortinc col dir - asc or desc)

And that's the plan, man...

also try:
q.values_list('cdid','asin')

"""

def editor(request):
    # note this 'processes' the result if nec. Doesn't do much, though.
    return HttpResponse(request.REQUEST["value"])

# this sucks, would be better to dynamically get fields...
cd_fields = ['cdid', 'asin', 'artist', 'title', 'upc']


# update a record. pass in cdid, asin,artist, title, upc
# would be better if just passed in actually changed fields tho
def updateCD(request):

    cdid = int(request.REQUEST['cdid'])
    asin = request.REQUEST['asin']
    artist = request.REQUEST['artist']
    title = request.REQUEST['title']
    upc = request.REQUEST['upc']
    logging.info("update yo. key = %i" % cdid)
    # test beelow
    record = CDRecord.objects.get(cdid = cdid)
    # update usin' model
    logging.info("record: %s" % str(record))
    record.asin = asin
    record.artist = artist
    record.title = title
    record.upc = upc
    record.save()
    return HttpResponse(cdid)
    
# addCD
# return is new cdid on success, nothing on fail.
def addCD(request):
    #cdid = int(request.REQUEST['cdid'])
    asin = request.REQUEST.get('asin')
    artist = request.REQUEST.get('artist')
    title = request.REQUEST.get('title')
    upc = request.REQUEST.get('upc')
    
    c = CDRecord(asin = asin, artist = artist, title = title, upc = upc)
    try:
        c.save()
    except Exception, val:
        return HttpResponse('%s:%s'%(Exception, val))
    return HttpResponse(c.cdid)

# deleteCD
def deleteCD(request):
    cdid = int(request.REQUEST['cdid'])
    try:
      record = CDRecord.objects.get(cdid = cdid)
      record.delete()
    except:
        cdid = 0
    return HttpResponse(cdid)
    

# generate the CHUNK of JSON the page will use, based on params like
# starting point, how many to show, how to sort...whittle down the set
def cds(request):
    iSortCol = []
    iColumns = int(request.REQUEST["iColumns"])
    sColumns = request.REQUEST["sColumns"]
    iDisplayStart = int(request.REQUEST["iDisplayStart"])
    iDisplayLength = int(request.REQUEST["iDisplayLength"])
    sSearch = request.REQUEST["sSearch"]
    iSortingCols = int(request.REQUEST['iSortingCols'])
    # cols are numbers. dir is asc or desc
    if iSortingCols:
        for i in range(iSortingCols):
          colly = cd_fields[int(request.REQUEST["iSortCol_" + str(i)])]
          if request.REQUEST["iSortDir_" + str(i)] == 'desc':
            colly = "-" + colly
          iSortCol.append(colly)
    
    # search filter first
    qSet = CDRecord.objects.all()
    totalRecords = qSet.count()
    if sSearch:
        qSets =  []
        for i in range(len(cd_fields)):
            kwargs = {"%s__icontains" % cd_fields[i]: sSearch}
            qSets.append(CDRecord.objects.filter(**kwargs))
        qSet = qSets[0]
        for qs in qSets[1:]:
            qSet = qSet | qs
            
    # sort shit, son!
    logging.debug("sorty " + str(iSortCol))
    # gotta strip down to reflect display start, display length
    # total num of records = num of rows in set...
    filteredRecords = qSet.count()
    stuff = makeData(qSet.order_by(*iSortCol)[iDisplayStart:iDisplayStart + iDisplayLength], iDisplayStart, filteredRecords, totalRecords)
    return HttpResponse(stuff)

#handle converting the raw set to desired JSON why you don't really need a template: all you're doing is generating JSON 
def makeData(qSet, displayStart, filteredRecords, totalRecords):
    data = {"iTotalRecords": totalRecords,"iTotalDisplayRecords": filteredRecords}
    aaData = []
    # iterate thru qSet
    for rec in qSet:
        aaData.append([unicode(getattr(rec,fld)) for fld in cd_fields])
    data["aaData"] = aaData
    return simplejson.dumps(data)


