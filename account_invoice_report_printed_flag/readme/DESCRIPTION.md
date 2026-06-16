This module extends ``account.move`` to support the printed flag
mechanism provided by the ``report_printed_flag`` module.

It adds printed report tracking capabilities to invoices,
bills, and journal entries.

It adds a ``printed`` field and integrates printed tracking features
into the accounting user interface.

Main features:

- Adds ``printed`` field to ``account.move``
- Tracks printed reports using the core module
- Displays printed report names per record (optional field)
- Provides direct access to printed logs
- Adds search filters:
  - Printed
  - Not Printed
- Adds group by:
  - Printed
  - Printed Report Names
- Supports multi-company configurations

Printed report names are computed from related printed logs and displayed
as a comma-separated string.