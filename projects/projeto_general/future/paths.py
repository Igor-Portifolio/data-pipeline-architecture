from projects.projeto_general.future.config import ClientConfig, FileType
from src.infra.io.paths import raw_data_file_path, logs_data_file_path, stagging_data_file_path, curated_data_file_path
from pathlib import Path


def build_paths(config: ClientConfig, *, revision: str = "RevA"):
    stem = Path(config.file_name).stem
    extension = config.file_type.value

    input_file_path = raw_data_file_path(config.file_name)

    staging_file_name = f"{stem}_staging.{extension}"
    logs_file_name = f"{stem}_logs.csv"
    final_file_name = f"{stem}_{revision}.{extension}"

    staging_file_path = stagging_data_file_path(staging_file_name)
    logs_file_path = logs_data_file_path(logs_file_name)
    curated_file_path = curated_data_file_path(final_file_name)

    return {
        "input": input_file_path,
        "staging": staging_file_path,
        "logs": logs_file_path,
        "curated": curated_file_path,
        "final_name": final_file_name,  # útil para logs/prints
        "revision": revision,
    }


if __name__ == "__main__":
    config = ClientConfig(
        file_name="projeto_teste.csv",
        file_type=FileType.CSV,
        string_columns=["nome", "status"],
        email_column="email",
        cpf_column=None,  # exemplo de coluna ausente
    )

    paths_a = build_paths(config)  # default RevA
    paths_b = build_paths(config, revision="RevB")

    print("\n--- Acessando individualmente ---")

    print("Input path:   ", paths_b["input"])
    print("Staging path: ", paths_b["staging"])
    print("Logs path:    ", paths_b["logs"])
    print("Curated path: ", paths_b["curated"])
    print("Final name:   ", paths_b["final_name"])
    print("Revision:     ", paths_b["revision"])
