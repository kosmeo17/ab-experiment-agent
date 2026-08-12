-- AB 实验助手使用日志（da_agent_data；DDL 由数据部在 MySQL 实例执行）
-- 文档: references/usage-logging.md

CREATE TABLE IF NOT EXISTS da_agent_data.ab_experiment_agent_log (
    log_id           VARCHAR(32)   NOT NULL COMMENT '日志ID',
    session_id       VARCHAR(32)   NOT NULL COMMENT '会话ID（design_start/stage_pass/design_end 成对）',
    user_name        VARCHAR(64)   NOT NULL COMMENT '中文名 英文名',
    department       VARCHAR(128)  NOT NULL COMMENT '部门',
    event_time       DATETIME      NOT NULL COMMENT '事件时间（东八区）',
    event_type       VARCHAR(32)   NOT NULL COMMENT 'setup|design_start|stage_pass|design_end',
    stage_code       VARCHAR(64)   NOT NULL COMMENT 'setup|session|session_complete|session_abort|g1_necessity|...|g9_formal_doc',
    stage_name       VARCHAR(64)   NOT NULL COMMENT '阶段中文名；design_end 用 session_complete=完整收口 / session_abort=中途结束',
    client_tool      VARCHAR(32)   NULL     COMMENT 'cursor|codex|claude',
    user_query       TEXT          NULL     COMMENT '用户原话',
    experiment_name  VARCHAR(512)  NULL     COMMENT '实验名称',
    result_summary   TEXT          NULL     COMMENT '阶段结果摘要',
    extra_json       TEXT          NULL     COMMENT '扩展JSON，禁止含token',
    PRIMARY KEY (log_id),
    KEY idx_session (session_id),
    KEY idx_user_time (user_name, event_time),
    KEY idx_event_stage (event_type, stage_code, event_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='AB实验助手使用日志（初始化/设计开始/Gate通过/设计结束）';
