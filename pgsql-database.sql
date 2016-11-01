-- -----------------------------------------------------
-- Table "subscription"
-- -----------------------------------------------------
DROP TABLE IF EXISTS "subscription";
DROP SEQUENCE IF EXISTS "subscription_id_seq";

CREATE TABLE IF NOT EXISTS "subscription" (
  "id"                SERIAL,
  "device"            VARCHAR(40)      NOT NULL,
  "service_id"        integer NOT NULL,
  "last_read"         integer NOT NULL DEFAULT 0,
  "timestamp_created" TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "timestamp_checked" TIMESTAMP            NULL DEFAULT NULL,
  PRIMARY KEY ("id")
);

-- -----------------------------------------------------
-- Table "message"
-- -----------------------------------------------------
DROP TABLE IF EXISTS "message";
DROP SEQUENCE IF EXISTS "message_id_seq";

CREATE TABLE IF NOT EXISTS "message" (
  "id"                SERIAL,
  "service_id"        integer NOT NULL,
  "text"              TEXT             NOT NULL,
  "title"             VARCHAR(255)         NULL  DEFAULT NULL,
  "level"             SMALLINT       NOT NULL DEFAULT 0,
  "link"              TEXT                 NULL,
  "timestamp_created" TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id")
);

-- -----------------------------------------------------
-- Table "service"
-- -----------------------------------------------------
DROP TABLE IF EXISTS "service";
DROP SEQUENCE IF EXISTS "service_id_seq";

CREATE TABLE IF NOT EXISTS "service" (
  "id"                SERIAL,
  "secret"            VARCHAR(32)      NOT NULL,
  "public"            VARCHAR(40)      NOT NULL,
  "name"              VARCHAR(255)     NOT NULL,
  "icon"              TEXT                 NULL,
  "timestamp_created" TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id")
);

-- -----------------------------------------------------
-- Table "gcm"
-- -----------------------------------------------------
DROP TABLE IF EXISTS "gcm";
DROP SEQUENCE IF EXISTS "gcm_id_seq";

CREATE TABLE IF NOT EXISTS "gcm" (
  "id"                SERIAL,
  "uuid"              VARCHAR(40)      NOT NULL,
  "gcmid"             TEXT             NOT NULL,
  "pubkey"            TEXT             DEFAULT NULL,
  "timestamp_created" TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "rsa_pub"           BYTEA       DEFAULT NULL,
  PRIMARY KEY ("id")
);

