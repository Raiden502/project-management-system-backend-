DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'roles') THEN
        CREATE TYPE roles as ENUM('super_admin', 'admin', 'user');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'message_types') THEN
        CREATE TYPE message_types as ENUM('info', 'image', 'file');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'priorities') THEN
        CREATE TYPE priorities as ENUM('low', 'medium', 'high');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'file_types') THEN
        CREATE TYPE file_types as ENUM('image', 'file');
    END IF;
END
$$;


CREATE TABLE IF NOT EXISTS  organization (
    organization_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_modified TIMESTAMP
);


--- Files ---

CREATE TABLE IF NOT EXISTS  files (
    file_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    file_src VARCHAR(1000) NOT NULL,
    file_type file_types NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT files_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id)
);

--- users ----

CREATE TABLE IF NOT EXISTS  user_info (
    user_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    email_addrs VARCHAR(255) UNIQUE NOT NULL,
    mobile_num VARCHAR(255),
    address VARCHAR(500),
    verified BOOLEAN DEFAULT FALSE NOT NULL,
    role roles NOT NULL,
    avatar TEXT,
    chat_socket_id VARCHAR(255) UNIQUE,
    video_socket_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    CONSTRAINT user_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id)
);

CREATE TABLE IF NOT EXISTS  group_info (
    group_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    avatar TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    CONSTRAINT group_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT group_created_by_fk FOREIGN KEY (created_by) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  messages (
    message_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    sender_id VARCHAR(255) NOT NULL,
    reciever_id VARCHAR(255),
    group_id VARCHAR(255),
    file_id VARCHAR(255),
    message VARCHAR(1000) NOT NULL,
    message_type message_types NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT messages_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT messages_sender_fk FOREIGN KEY (sender_id) REFERENCES user_info (user_id),
    CONSTRAINT messages_reciever_fk FOREIGN KEY (reciever_id) REFERENCES user_info (user_id),
    CONSTRAINT messages_group_fk FOREIGN KEY (group_id) REFERENCES group_info (group_id),
    CONSTRAINT messages_file_fk FOREIGN KEY (file_id) REFERENCES files (file_id)
);

CREATE TABLE IF NOT EXISTS  user_group_associaton (
    relation_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    group_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT usergroup_user_association_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id),
    CONSTRAINT usergroup_group_association_fk FOREIGN KEY (group_id) REFERENCES group_info (group_id)
);

--- departments ---

CREATE TABLE IF NOT EXISTS  department_info (
    department_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    avatar TEXT,
    associate_user VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_modified TIMESTAMP,
    project_count BIGINT DEFAULT 0,
    task_count BIGINT DEFAULT 0,
    teams_count BIGINT DEFAULT 0,
    users_count BIGINT DEFAULT 0,
    CONSTRAINT dept_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT dept_creator_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id),
    CONSTRAINT dept_associate_fk FOREIGN KEY (associate_user) REFERENCES user_info (user_id)
);


CREATE TABLE IF NOT EXISTS  dept_user_associaton (
    relation_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT dept_user_association_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id),
    CONSTRAINT deptuser_dept_association_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id)
);


--- Projects  ---

CREATE TABLE IF NOT EXISTS  projects_info (
    project_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_modified TIMESTAMP,
    task_count BIGINT DEFAULT 0,
    teams_count BIGINT DEFAULT 0,
    users_count BIGINT DEFAULT 0,
    CONSTRAINT projects_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT projects_department_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id),
    CONSTRAINT projects_creator_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  project_user_association (
    relation_id VARCHAR(255) PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT project_user_association_project_fk FOREIGN KEY (project_id) REFERENCES projects_info (project_id),
    CONSTRAINT project_user_association_department_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id),
    CONSTRAINT project_user_association_user_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id)
);

--- Teams ---

CREATE TABLE IF NOT EXISTS  teams_info (
    team_id VARCHAR(255) PRIMARY KEY,
    organization_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    avatar VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    user_count BIGINT DEFAULT 0,
    CONSTRAINT teams_organization_fk FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT teams_department_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id),
    CONSTRAINT teams_created_by_fk FOREIGN KEY (created_by) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  team_user_associaton (
    relation_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    team_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT team_user_association_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id),
    CONSTRAINT teamuser_user_association_fk FOREIGN KEY (team_id) REFERENCES teams_info (team_id)
);

--- Tasks ---

CREATE TABLE IF NOT EXISTS  task_types (
    type_id VARCHAR(255) PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT task_types_project_fk FOREIGN KEY (project_id) REFERENCES projects_info (project_id),
    CONSTRAINT task_types_department_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id),
    CONSTRAINT task_types_created_by_fk FOREIGN KEY (created_by) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  tasks (
    task_id VARCHAR(255) PRIMARY KEY,
    type_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    department_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    labels TEXT [],
    created_by VARCHAR(255) NOT NULL,
    reporter VARCHAR(255),
    priority priorities NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    due_date TIMESTAMP,
    CONSTRAINT tasks_type_fk FOREIGN KEY (type_id) REFERENCES task_types (type_id),
    CONSTRAINT tasks_project_fk FOREIGN KEY (project_id) REFERENCES projects_info (project_id),
    CONSTRAINT tasks_department_fk FOREIGN KEY (department_id) REFERENCES department_info (department_id),
    CONSTRAINT tasks_created_by_fk FOREIGN KEY (created_by) REFERENCES user_info (user_id),
    CONSTRAINT tasks_reporter_fk FOREIGN KEY (reporter) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  task_files_associaton (
    relation_id VARCHAR(255) PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL,
    file_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT task_files_association_task_fk FOREIGN KEY (task_id) REFERENCES tasks (task_id),
    CONSTRAINT task_files_association_file_fk FOREIGN KEY (file_id) REFERENCES files (file_id)
);

CREATE TABLE IF NOT EXISTS  task_user_association (
    relation_id VARCHAR(255) PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL,
    task_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT task_user_association_project_fk FOREIGN KEY (project_id) REFERENCES projects_info (project_id),
    CONSTRAINT task_user_association_task_fk FOREIGN KEY (task_id) REFERENCES tasks (task_id),
    CONSTRAINT task_user_association_user_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id)
);

CREATE TABLE IF NOT EXISTS  comments (
    comment_id VARCHAR(255) PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    message VARCHAR(255) NOT NULL,
    message_type message_types NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT comments_task_fk FOREIGN KEY (task_id) REFERENCES tasks (task_id),
    CONSTRAINT comments_project_fk FOREIGN KEY (project_id) REFERENCES projects_info (project_id),
    CONSTRAINT comments_user_fk FOREIGN KEY (user_id) REFERENCES user_info (user_id)
);