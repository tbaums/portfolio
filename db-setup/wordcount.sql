/* 
Drop the table if it exists
*/
drop table if exists "public"."wordcount";

/* 
Create table
*/
create table "public"."wordcount" (
    id serial primary key,
    search_param_id int,
    analysis text,
    CONSTRAINT search_param_id FOREIGN KEY (search_param_id) REFERENCES public.search_params (id)  
);

/*
Create an index on parameters so it isn't miserably slow
*/
create index search_param_id_index ON "public"."wordcount" (search_param_id);