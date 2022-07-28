package search

import java.io.File
import kotlin.collections.mutableListOf

fun inputOfData(filePath: String): List<String> {
    val dataFile = File(filePath)

    return dataFile.readLines()
}

fun queryData(listToQuery: List<String>) {
    val results = mutableListOf<String>()
    println("Enter a name or email to search all matching people.")
    val query = readln()

    for (item in listToQuery) if (item.contains(query, ignoreCase = true)) results.add(item)

    if (results.isEmpty()) println("No results") else results.forEach { println(it) }

    menu(listToQuery)
}

fun menu(dataForMenu: List<String>) {
    println("=== Menu ===\n1. Find a person\n2. Print all people\n0. Exit")
    when (readln()) {
        "1" -> {
            queryData(dataForMenu)
        }
        "2" -> {
            for (item in dataForMenu) println(item)
            menu(dataForMenu)
        }
        "0" -> println("Bye!")
        else -> {
            println("Incorrect option! Try again.")
            menu(dataForMenu)
        }
    }
}

fun main(args: Array<String>) {

    val dataFromFile = inputOfData(args[1])
    menu(dataFromFile)
}
