CREATE TABLE match_general_info(
    match_id int not null primary key,
    league varchar(50),
    season char(9),
    day_of_week char(3),
    date date,
    starttime time,
    stadium varchar(50),
    num_attendance int,
    referee varchar(50),
    hometeam_id int,
    awayteam_id int,
    hometeam_name varchar(50),
    awayteam_name varchar(50),
    hometeam_score int,
    awayteam_score int,
    hometeam_rank int,
    awayteam_rank int,
    primary key(match_id),
    constraint fk_hometeam_id
        foreign key(hometeam_id)
        references teams(team_id)
    constraint fk_awayteam_id
        foreign key(awayteam_id)
        references teams(teamd_id)
    );