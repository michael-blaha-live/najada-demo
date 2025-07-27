graph TD
    A[Start: User arrives at shop] --> B{Browse Menu};

    B --> C[GET /api/eshop/menu-items];
    B --> D[GET /api/eshop/dough-types];
    B --> E[GET /api/eshop/ingredients];

    C --> F{Select Baguette};
    D --> G{Select Dough Type};
    F & G --> H{Enter Quantity & Note};

    H --> I[POST /api/eshop/cart/items];

    I --> J{Item Added to Cart?};
    J -- No (Unavailable) --> K[Display Error: Item Unavailable];
    J -- Yes (Success) --> L[View Updated Cart];

    L --> M{Decision: Continue Shopping or Checkout?};
    M -- Continue Shopping --> B;
    M -- Checkout --> N[GET /api/eshop/cart/];

    N --> O{Review Cart Contents};
    O --> P{Decision: Cart OK?};
    P -- No (Change Qty) --> Q[PATCH /api/eshop/cart/items/:id];
    P -- No (Remove Item) --> R[DELETE /api/eshop/cart/items/:id];
    Q & R --> L;
    P -- Yes (Proceed) --> S[GET /api/eshop/payment-types/];

    S --> T{Select Payment Type};
    T --> U[POST /api/eshop/orders/create/];

    U --> V{Order Placed?};
    V -- No (Order Failed) --> W[Display Error: Order Failed];
    V -- Yes (201 Created) --> X[Display Order Confirmation];

    X --> Y[GET /api/eshop/orders/:id/];
    X --> Z[GET /api/eshop/orders/];
    Y & Z --> AA[End: Order Tracking/Completion];

    K --> B;
    W --> L;
