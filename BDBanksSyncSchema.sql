-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.logs (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid,
  service_name text NOT NULL,
  action text NOT NULL,
  message text NOT NULL,
  properties jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT logs_pkey PRIMARY KEY (id),
  CONSTRAINT logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.reconciliations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  upload_id uuid NOT NULL,
  name text NOT NULL,
  status text NOT NULL DEFAULT 'draft'::text,
  summary jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT reconciliations_pkey PRIMARY KEY (id),
  CONSTRAINT reconciliations_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES public.uploads(id)
);
CREATE TABLE public.reports (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  reconciliation_id uuid NOT NULL,
  title text NOT NULL,
  storage_path text NOT NULL,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT reports_pkey PRIMARY KEY (id),
  CONSTRAINT reports_reconciliation_id_fkey FOREIGN KEY (reconciliation_id) REFERENCES public.reconciliations(id)
);
CREATE TABLE public.transactions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  upload_id uuid NOT NULL,
  amount numeric NOT NULL,
  currency text NOT NULL DEFAULT 'USD'::text,
  internal_reference text,
  external_reference text,
  raw_data jsonb NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT transactions_pkey PRIMARY KEY (id),
  CONSTRAINT transactions_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES public.uploads(id)
);
CREATE TABLE public.uploads (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  original_filename text NOT NULL,
  storage_path text NOT NULL,
  status text NOT NULL DEFAULT 'uploaded'::text,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT uploads_pkey PRIMARY KEY (id),
  CONSTRAINT uploads_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.users (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  email text NOT NULL,
  full_name text,
  role text NOT NULL DEFAULT 'viewer'::text,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT users_pkey PRIMARY KEY (id)
);
CREATE TABLE public.workflows (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  is_active boolean NOT NULL DEFAULT true,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT workflows_pkey PRIMARY KEY (id)
);