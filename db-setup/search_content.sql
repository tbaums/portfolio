/* 
Drop the table if it exists
*/
drop table if exists "public"."search_content" cascade;

/* 
Create table
*/
create table "public"."search_content" (
    id serial primary key,
    search_param_id  int,
    source_id text,
    source_name text,
    author text,
    title text,
    "description" text,
    "url" text,
    "url_to_image" text,
    published_at text,
    CONSTRAINT search_param_id FOREIGN KEY (search_param_id) REFERENCES public.search_params (id)  
    );

