from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "school" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "faculty" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "school_id" INT NOT NULL REFERENCES "school" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_faculty_school__647fa3" UNIQUE ("school_id", "name")
);
CREATE TABLE IF NOT EXISTS "programme" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "level_count" INT NOT NULL,
    "level_label" VARCHAR(50) NOT NULL DEFAULT 'Level',
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "faculty_id" INT NOT NULL REFERENCES "faculty" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_programme_faculty_16d2b7" UNIQUE ("faculty_id", "name")
);
CREATE TABLE IF NOT EXISTS "level" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "number" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "programme_id" INT NOT NULL REFERENCES "programme" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_level_program_fcb53c" UNIQUE ("programme_id", "number")
);
CREATE TABLE IF NOT EXISTS "course" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "code" VARCHAR(50),
    "name" VARCHAR(255) NOT NULL,
    "semester" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "level_id" INT NOT NULL REFERENCES "level" ("id") ON DELETE CASCADE,
    "programme_id" INT NOT NULL REFERENCES "programme" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_course_program_7dcad2" UNIQUE ("programme_id", "level_id", "semester", "code")
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "onboarded" INT NOT NULL DEFAULT 0,
    "role" VARCHAR(7) NOT NULL DEFAULT 'student' /* STUDENT: student\nADMIN: admin\nROOT: root */,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "level_id" INT REFERENCES "level" ("id") ON DELETE SET NULL,
    "programme_id" INT REFERENCES "programme" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_user_program_11c1c2" ON "user" ("programme_id", "level_id");
CREATE TABLE IF NOT EXISTS "material" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "material_type" VARCHAR(14) /* SLIDES: slides\nPAST_QUESTIONS: past_questions\nCOURSE_OUTLINE: course_outline\nTIMETABLE: timetable\nBOOK: book\nOTHER: other */,
    "academic_year" INT,
    "semester" INT,
    "telegram_file_id" VARCHAR(255) NOT NULL,
    "telegram_chat_id" BIGINT NOT NULL,
    "telegram_message_id" BIGINT NOT NULL,
    "file_name" VARCHAR(255) NOT NULL,
    "mime_type" VARCHAR(100),
    "file_size" BIGINT,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE,
    "uploaded_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_material_course__8a9f6d" ON "material" ("course_id", "material_type");
CREATE INDEX IF NOT EXISTS "idx_material_course__eefd41" ON "material" ("course_id", "academic_year");
CREATE INDEX IF NOT EXISTS "idx_material_course__ceaaf8" ON "material" ("course_id", "semester");
CREATE TABLE IF NOT EXISTS "materialrequest" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "material_type" VARCHAR(14) NOT NULL /* SLIDES: slides\nPAST_QUESTIONS: past_questions\nCOURSE_OUTLINE: course_outline\nTIMETABLE: timetable\nBOOK: book\nOTHER: other */,
    "semester" INT,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "course_id" INT NOT NULL REFERENCES "course" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_materialreq_course__596802" ON "materialrequest" ("course_id", "material_type");
CREATE INDEX IF NOT EXISTS "idx_materialreq_course__fe00de" ON "materialrequest" ("course_id", "semester");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
