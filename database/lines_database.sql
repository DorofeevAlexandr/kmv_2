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
    connection_counters  bigint[]
);

CREATE index IF NOT EXISTS times_time_idx ON times(time);
