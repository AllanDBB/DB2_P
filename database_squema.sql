-- Dominios
CREATE TABLE IF NOT EXISTS public.countries (
  code text PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE IF NOT EXISTS public.categories (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL UNIQUE
);

-- Comercial
CREATE TABLE IF NOT EXISTS public.products (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  category_id bigint NOT NULL REFERENCES public.categories(id),
  unit_price numeric(12,2) NOT NULL CHECK (unit_price >= 0),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.customers (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name text NOT NULL,
  email text,
  country_code text NOT NULL REFERENCES public.countries(code),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.invoices (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES public.customers(id),
  invoice_date date NOT NULL DEFAULT current_date,
  total_amount numeric(14,2) NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.invoice_lines (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  invoice_id bigint NOT NULL REFERENCES public.invoices(id) ON DELETE CASCADE,
  product_id bigint NOT NULL REFERENCES public.products(id),
  quantity numeric(12,2) NOT NULL CHECK (quantity > 0),
  unit_price numeric(12,2) NOT NULL CHECK (unit_price >= 0),
  line_total numeric(14,2) NOT NULL CHECK (line_total >= 0)
);

-- Tablas de autorización (RLS)
CREATE TABLE IF NOT EXISTS public.user_allowed_country (
  user_id uuid NOT NULL REFERENCES auth.users(id),
  country_code text NOT NULL REFERENCES public.countries(code),
  PRIMARY KEY (user_id, country_code)
);

CREATE TABLE IF NOT EXISTS public.user_allowed_category (
  user_id uuid NOT NULL REFERENCES auth.users(id),
  category_id bigint NOT NULL REFERENCES public.categories(id),
  PRIMARY KEY (user_id, category_id)
);

-- Activar RLS
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoice_lines ENABLE ROW LEVEL SECURITY;

-- 5. Políticas (ejemplos, puedes extenderlas según PDF)

-- Products por categoría
CREATE POLICY "products_by_user_category_select"
ON public.products FOR SELECT
TO authenticated
USING (EXISTS (
  SELECT 1 FROM public.user_allowed_category u
  WHERE u.user_id = auth.uid() 
  AND u.category_id = products.category_id
));

-- Customers por país
CREATE POLICY "customers_by_user_country_select"
ON public.customers FOR SELECT
TO authenticated
USING (EXISTS (
  SELECT 1 FROM public.user_allowed_country u
  WHERE u.user_id = auth.uid() 
  AND u.country_code = customers.country_code
));

-- Invoices por país (ligado al cliente)
CREATE POLICY "invoices_by_user_country_select"
ON public.invoices FOR SELECT
TO authenticated
USING (EXISTS (
  SELECT 1
  FROM public.customers c
  JOIN public.user_allowed_country u
    ON u.country_code = c.country_code 
    AND u.user_id = auth.uid()
  WHERE c.id = invoices.customer_id
));

-- Invoice lines por país y categoría
CREATE POLICY "lines_by_country_and_category_select"
ON public.invoice_lines FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1
    FROM public.invoices i
    JOIN public.customers c ON c.id = i.customer_id
    JOIN public.user_allowed_country uc
      ON uc.country_code = c.country_code 
      AND uc.user_id = auth.uid()
    WHERE i.id = invoice_lines.invoice_id
  )
  AND
  EXISTS (
    SELECT 1
    FROM public.products p
    JOIN public.user_allowed_category ug
      ON ug.category_id = p.category_id 
      AND ug.user_id = auth.uid()
    WHERE p.id = invoice_lines.product_id
  )
);
