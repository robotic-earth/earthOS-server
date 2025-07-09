#include <stdio.h>
#include <string.h>

int main() {
    FILE *config = fopen("config.txt", "r");
    if (config == NULL)
    {
       printf("could not find configuration file\n");
       return 1;
    }
    
    char line[256];
    int api_only_mode = 0;

    while (fgets(line, sizeof(line), config))
    {
       if (strstr(line, "API_ONLY_MODE=1"))
       {
        api_only_mode = 1;
        break;
       }
    }
    
    fclose(config);

    if (api_only_mode)
    {
        printf("running API only mode\n");
    } 
    else
    {
        printf("web ui active\n");
    }

    return 0;
}