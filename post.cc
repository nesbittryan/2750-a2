#include<stdlib.h>
#include<string.h>
#include<stdio.h>
#include<time.h>
#include"stream.h"

class PostEntry {
    void readInput(char * stream, char * text) {
        printf("Stream: ");
        fgets(stream, 99, stdin);
        if(stream[0] == '\n') {
            printf("Stream must be identified...\n");
            exit(-1);
        }
        printf("Enter text: ");
        strcpy(text, "");
        char string[80];
        while(fgets(string, 79, stdin)) {
            printf("-");
            strcat(text, string);
        }
        printf("\n");
    }

    void formatEntry(struct userPost *up, char * name, char * stream, char * text, char * date) {
        up->username = (char*)malloc(sizeof(char) * strlen(name) + 1);
        up->streamname = (char*)malloc(sizeof(char) * strlen(stream) + 1);
        up->text = (char*)malloc(sizeof(char) * strlen(text) + 1);
        up->date = (char*)malloc(sizeof(char) * strlen(date) + 1);
        strcpy(up->username, name);
        int i;
        for(i = strlen(stream); i >= 0; --i) {
            if(stream[i] == ' ' || stream[i] == '\n') {
                stream[i] = '\0';
            }
        }
        strcpy(up->streamname, stream);
        strcpy(up->text, text);
        strcpy(up->date, date);
    }

    void getTimeDate(char * date) {
        char copy[100];
        time_t t = time(NULL);
        struct tm tm = *localtime(&t);
        switch(tm.tm_mon + 1) {
            case 1:
                strcpy(date, "Jan. ");
                break;
            case 2:
                strcpy(date, "Feb. ");
                break;
            case 3:
                strcpy(date, "Mar. ");
                break;
            case 4:
                strcpy(date, "Apr. ");
                break;
            case 5:
                strcpy(date, "May. ");
                break;
            case 6:
                strcpy(date, "Jun. ");
                break;
            case 7:
                strcpy(date, "Jul. ");
                break;
            case 8:
                strcpy(date, "Aug. ");
                break;
            case 9:
                strcpy(date, "Sep. ");
                break;
            case 10:
                strcpy(date, "Oct. ");
                break;
            case 11:
                strcpy(date, "Nov. ");
                break;
            case 12:
                strcpy(date, "Dec. ");
                break;
        }

        sprintf(copy, "%d,", tm.tm_mday);
        strcat(date, copy);
        strcat(date, " ");
        sprintf(copy, "%d,", tm.tm_year + 1900);
        strcat(date, copy);
        if(tm.tm_hour < 12) {
            sprintf(copy, "%d:%d", tm.tm_hour, tm.tm_min);
            strcat(date, copy);
            strcat(date, " AM");
        } else {
            if(tm.tm_hour == 12) {
                sprintf(copy, " %d:%02d", tm.tm_hour, tm.tm_min);
            } else {
                sprintf(copy, " %d:%02d", tm.tm_hour - 12, tm.tm_min);
            }
            strcat(date, copy);
            strcat(date, " PM");
        }
    }
    void submitPost(struct userPost sp) {
        updateStream(&sp);
        free(sp.username);
        free(sp.streamname);
        free(sp.date);
        free(sp.text);
        return;
    }
};

int main(int argc, char ** argv) {
    if(argv[1] == NULL) {
        printf("Username must be entered...\n");
        return(-1);
    }
    int i = 2;
    char name[100], stream[100], text[1000], date[100];
    strcpy(name, argv[1]);
    while(argv[i] != NULL) {
        strcat(name, " ");
        strcat(name, argv[i]);
        ++i;
    }
    struct userPost up;
    class PostEntry myPost;
    myPost.readInput(&stream[0], &text[0]);
    myPost.getTimeDate(&date[0]);
    myPost.formatEntry(&up, name, stream, text, date);
    myPost.submitPost(up);
    return (0);
}
