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


OPDS compatible E-reader apps
=============================

- Aldiko (Android): http://www.aldiko.com/

- Bluefire (Android, iOS): http://www.bluefirereader.com/

- FBreader (Android, Symbian, Meego etc.): http://www.fbreader.org/
 
- Stanza (acquired by Amazon.com and discontinued)


Roadmap
=======

ENT-01 Catalog Root (Últimos livros, Editoras, Ordem alfabética) *1

ENT-03 Partial Catalog Entry (Acquisition Feed) *1

ENT-04 Complete Catalog Entry (Com suporte a paginação) *1

ENT-05 Integração com WS da Scielo para Catalog Root/Entry

ENT-06 Integração com WS da Scielo para Catalog Entry

ENT-07 Suporte a compactação e caching [lado da aplicação]

ENT-08 Definição e acompanhamento no deploy


[1] Utilizando fixtures fornecidas pela Scielo