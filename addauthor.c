#include "stream.h"

int main(int argc, char ** argv) {
    int i = 1, rFlag = 0;
    if(argc == 1) {
        printf("Include username...\n");
        return(-1);
    }
    if(strcmp(argv[i], "-r") == 0) {
        rFlag = 1;
        ++i;
    }
    if(argv[i] == NULL) {
        printf("Include username...\n");
        return(-1);
    }
    char * username = malloc(sizeof(char) * 100);
    char streams[100];
    strcpy(username, argv[i]);
    ++i;
    while(argv[i] != NULL) {
        strcat(username, " ");
        strcat(username, argv[i]);
        ++i;
    }
    printf("List streams: ");
    fgets(streams, 99, stdin);
    streams[strlen(streams)-1] = '\0';
    int j;
    for(i = 0; i < strlen(streams); ++i) {
        if(streams[i] == ' ') {
            for(j = i; j < strlen(streams) - 1; ++j) {
                streams[j] = streams[j+1];
            }
            streams[strlen(streams)-1] = '\0';
        }
    }
    if(rFlag == 1) {
        removeUser(username, streams);
    } else {
        addUser(username, streams);
    }
    free(username);
    return(0);
}
