Knitting_Chart_Maker/
|-- design-notes/
|-- src/
|   |-- adapters/       # Adapter layer
|   |-- application/    # Application services layer
|   |-- domain/         # Domain layer
|   |   |-- model/          # Domain model entities and value objects
|   |   |-- parser/         # Parser logic and entities
|   |-- infrastructure/ # Framework-specific adapters
|   |-- ports/          # Ports layer
|   |   |-- logger/         # Logger port
|   |-- routers/        # API routers

----------------------------------------------------------------------
Attribution: Folder structure was inspired by Hieu Tran in their article [Building Maintainable Python Applications with Hexagonal Architecture and Domain-Driven Design](https://dev.to/hieutran25/building-maintainable-python-applications-with-hexagonal-architecture-and-domain-driven-design-chp)