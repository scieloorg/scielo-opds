=============================
OPDS support for SciELO Books
=============================

This is an implementation of an Open Publication Distribution System (OPDS_)
catalog for the SciELO Books application.

.. _OPDS: http://opds-spec.org/

---------
Objective
---------

To allow a user with an OPDS compatible e-reader application or device to
browse the catalog of books available through the SciELO Books portal.

------------
Requirements
------------

- OPDS 1.1 compliant implementation, validated through Benoît Larroque's 
  validator_

.. _validator: http://opds-validator.appspot.com/

- navigability and data quality verified via manual testing with an OPDS
  compatible e-reader application

- navigation feed with links sorted by title, author, subject, publisher, 
  acquisition type (open-access, buy)
  
- one acquisition feed per publisher


Requirements for a future contract
==================================

The following features are outside the scope of this job and will not be 
implemented at this time:
  
- search

- dedicated crawlable feeds (for bulk download of metadata)


OPDS compatible E-reader apps
=============================

- Aldiko (Android): http://www.aldiko.com/

- Bluefire (Android, iOS): http://www.bluefirereader.com/

- FBreader (Android, Symbian, Meego etc.): http://www.fbreader.org/
 
- Stanza (acquired by Amazon.com and discontinued)
  

-------
Roadmap
-------

2012-02-13 
    deployable app, serving metadata from a small fixture of catalog records

2012-02-20
    one navigation feed acquiring metadata from SciELO Books via a Web service

2012-02-27
    all views acquiring metadata from SciELO Books via Web services
