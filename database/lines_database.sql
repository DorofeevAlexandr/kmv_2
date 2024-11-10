--time
CREATE TABLE IF NOT EXISTS times (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY key,
    time timestamp NOT NULL
);

--counters_values
CREATE TABLE IF NOT EXISTS counters_values (
    id INTEGER REFERENCES times ON DELETE CASCADE,
    lengths  bigint[]
);

--connections_with_counters
CREATE TABLE IF NOT EXISTS connections_with_counters (
    id INTEGER REFERENCES times ON DELETE CASCADE,
    connection_counters  Boolean[]
);

CREATE index IF NOT EXISTS times_time_idx ON times(time);


--lines
CREATE TABLE IF NOT EXISTS lines (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY key,
    line_number INTEGER  NOT NULL unique,
    name char NOT NULL unique,
    port char NOT NULL,
    modbus_adr Integer NOT NULL,
    k  Float NOT NULL,
    created_dt timestamp,
	description text
);

--lines_current_params
CREATE TABLE IF NOT EXISTS lines_current_params (
    id INTEGER REFERENCES lines ON DELETE CASCADE,
    no_connection_counter Boolean,
    indicator_value Integer,
    length Float,
    speed_line Float,
    updated_dt timestamp
);
