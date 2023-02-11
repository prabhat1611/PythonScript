import yaml
import csv
import glob


yaml_file_names = glob.glob('./config.yaml')

rows_to_write = []
group_levels = ["demandtag-level-rules","router-level-rules","device-resolver-level-rules","geo-resolver-level-rules"]

for i, each_yaml_file in enumerate(yaml_file_names):
    print("Processing file {} of {} file name: {}".format(
        i+1, len(yaml_file_names),each_yaml_file))

    with open(each_yaml_file) as file:
        data = yaml.safe_load(file)
        for group_level in group_levels:
            for groups in data["additionalPrometheusRulesMap"][group_level]["groups"]:
                for rules in groups["rules"]:
                    values=dict()
                    values["group_level"] = group_level
                    values["group_name"] = groups["name"]
                    values["alert_name"] = rules["alert"]
                    values["for"] = rules["for"]
                    values["expr"] = rules["expr"]
                    values["severity"] = rules["labels"]["severity"]
                    values["description"] = rules["annotations"]["description"]
                   
                    if rules["labels"].get("time_offset") != None:
                        values["offset"] = rules["labels"]["time_offset"]
                    else:
                        values["offset"] = "N/A"
                    
                    rows_to_write.append([values["group_level"],values["group_name"],values["alert_name"],values["for"],values["severity"],values["offset"],values["description"],values["expr"]])

                

with open('output_csv_file.csv', 'w', newline='') as out:
    csv_writer = csv.writer(out)
    csv_writer.writerow(["group_level","group_name","alert_name","for","severity","offset","description","expression"])
    csv_writer.writerows(rows_to_write)
    print("Output file output_csv_file.csv created")
