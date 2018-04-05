/* 
Drop the table if it exists
*/
drop table if exists "public"."search_content";

/* 
Create table
*/
create table "public"."search_content" (
    id serial primary key,
    search_param_id  int,
    source_id int,
    source_name varchar(255),
    author varchar(255),
    title text,
    "description" text,
    "url" text,
    "url_to_image" text,
    published_at varchar(255),
    CONSTRAINT search_param_id FOREIGN KEY (search_param_id) REFERENCES public.search_params (id)  
    );

