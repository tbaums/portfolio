/* 
Drop the table if it exists
*/
drop table if exists "public"."search_params";

/* 
Create table
*/
create table "public"."search_params" (
    id serial primary key,
    parameters text 
);

/*
Create an index on parameters so it isn't miserably slow
*/
create index parameters_index ON "public"."search_params" (paramaters);