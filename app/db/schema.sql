SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: bg_reading_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.bg_reading_type AS ENUM (
    'mmol/l',
    'mg/dl'
);


--
-- Name: diabetes_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.diabetes_type AS ENUM (
    'type1',
    'type2'
);


--
-- Name: food_qty_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.food_qty_type AS ENUM (
    'g',
    'kg',
    'l',
    'ml',
    'nos'
);


--
-- Name: food_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.food_type AS ENUM (
    'breakfast',
    'lunch',
    'dinner',
    'snacks'
);


--
-- Name: insulin_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.insulin_type AS ENUM (
    'rapid_insulin_food',
    'rapid_insulin_correction',
    'long_acting_insulin'
);


--
-- Name: ratio_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ratio_type AS ENUM (
    'same',
    'time_range'
);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bg_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bg_log (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    client_id uuid NOT NULL,
    entry_datetime timestamp without time zone NOT NULL,
    bg_level numeric(10,2) NOT NULL,
    insulin_qty numeric(10,2) NOT NULL,
    insulin_type public.insulin_type NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: carb_ratio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.carb_ratio (
    id uuid NOT NULL,
    client_id uuid NOT NULL,
    ratio_type public.ratio_type NOT NULL,
    carb_ratio numeric(10,2) NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    insulin_sensitivity numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: clients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clients (
    id uuid NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    date_of_birth date,
    diabetes_type public.diabetes_type,
    bg_reading_type public.bg_reading_type,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: food_carb; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.food_carb (
    id uuid NOT NULL,
    food_name character varying(255) NOT NULL,
    food_qty_type public.food_qty_type NOT NULL,
    food_qty numeric(10,2) NOT NULL,
    carb_count numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: food_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.food_log (
    id uuid NOT NULL,
    entry_datetime timestamp without time zone NOT NULL,
    food_type public.food_type NOT NULL,
    food_carb_id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    is_active boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: bg_log bg_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bg_log
    ADD CONSTRAINT bg_log_pkey PRIMARY KEY (id);


--
-- Name: carb_ratio carb_ratio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carb_ratio
    ADD CONSTRAINT carb_ratio_pkey PRIMARY KEY (id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: food_carb food_carb_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.food_carb
    ADD CONSTRAINT food_carb_pkey PRIMARY KEY (id);


--
-- Name: food_log food_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.food_log
    ADD CONSTRAINT food_log_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: bg_log bg_log_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bg_log
    ADD CONSTRAINT bg_log_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id) ON DELETE CASCADE;


--
-- Name: bg_log bg_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bg_log
    ADD CONSTRAINT bg_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: carb_ratio carb_ratio_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.carb_ratio
    ADD CONSTRAINT carb_ratio_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: food_log food_log_food_carb_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.food_log
    ADD CONSTRAINT food_log_food_carb_id_fkey FOREIGN KEY (food_carb_id) REFERENCES public.food_carb(id);


--
-- Name: food_log food_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.food_log
    ADD CONSTRAINT food_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20210729175125'),
    ('20210729175351'),
    ('20210729175952'),
    ('20210729180410'),
    ('20210729181358'),
    ('20210729184518');
