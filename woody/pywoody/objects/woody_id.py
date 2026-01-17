class WoodyID():
        
    def create(
        self, 
        project_name: str, 
        context: list = None, 
        product_type: str = None,
        product_name: str = None,
        version: int = None
    ):
        id_base = "woodyid:"
        
        # Build context
        id = id_base + project_name
        if context:
            for i in range(min(3, len(context))):
                id += f"|{context[i]}"
        
        # Add product
        if product_type or product_name:
            id += ":"
            if product_type:
                id += product_type
            if product_name:
                id += f"|{product_name}"
        
        # Add version
        if version is not None:
            id += f"=v{version}"
            
        return id